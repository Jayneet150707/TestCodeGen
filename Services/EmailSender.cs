using EmailService.Models;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System.Net;
using System.Net.Mail;
using System.Text.Json;

namespace EmailService.Services;

public class EmailSender : IEmailSender
{
    private readonly EmailConfiguration _emailConfig;
    private readonly ILogger<EmailSender> _logger;
    private readonly string _queueFolder;

    public EmailSender(IOptions<EmailConfiguration> emailConfig, ILogger<EmailSender> logger)
    {
        _emailConfig = emailConfig.Value;
        _logger = logger;
        _queueFolder = Path.Combine(_emailConfig.AttachmentFolder, "Queue");
        
        // Ensure directories exist
        EnsureDirectoriesExist();
    }

    private void EnsureDirectoriesExist()
    {
        try
        {
            Directory.CreateDirectory(_emailConfig.AttachmentFolder);
            Directory.CreateDirectory(_queueFolder);
            Directory.CreateDirectory(_emailConfig.ProcessedFolder);
            Directory.CreateDirectory(_emailConfig.ErrorFolder);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to create required directories");
        }
    }

    public async Task<bool> SendEmailAsync(EmailRequest emailRequest)
    {
        try
        {
            using var client = new SmtpClient(_emailConfig.SmtpServer, _emailConfig.SmtpPort);
            client.EnableSsl = _emailConfig.EnableSsl;
            client.UseDefaultCredentials = false;
            client.Credentials = new NetworkCredential(_emailConfig.SmtpUsername, _emailConfig.SmtpPassword);

            using var message = new MailMessage();
            message.From = new MailAddress(_emailConfig.FromEmail, _emailConfig.FromName);
            
            // Add recipients
            foreach (var email in emailRequest.To.Split(';', StringSplitOptions.RemoveEmptyEntries))
            {
                message.To.Add(email.Trim());
            }

            // Add CC recipients
            if (!string.IsNullOrEmpty(emailRequest.Cc))
            {
                foreach (var email in emailRequest.Cc.Split(';', StringSplitOptions.RemoveEmptyEntries))
                {
                    message.CC.Add(email.Trim());
                }
            }

            // Add BCC recipients
            if (!string.IsNullOrEmpty(emailRequest.Bcc))
            {
                foreach (var email in emailRequest.Bcc.Split(';', StringSplitOptions.RemoveEmptyEntries))
                {
                    message.Bcc.Add(email.Trim());
                }
            }

            message.Subject = emailRequest.Subject;
            message.Body = emailRequest.Body;
            message.IsBodyHtml = emailRequest.IsHtml;

            // Set priority
            message.Priority = emailRequest.Priority switch
            {
                1 => MailPriority.High,
                3 => MailPriority.Low,
                _ => MailPriority.Normal
            };

            // Add attachments
            foreach (var attachmentPath in emailRequest.Attachments)
            {
                if (File.Exists(attachmentPath))
                {
                    var attachment = new Attachment(attachmentPath);
                    message.Attachments.Add(attachment);
                }
                else
                {
                    _logger.LogWarning("Attachment file not found: {AttachmentPath}", attachmentPath);
                }
            }

            await client.SendMailAsync(message);
            _logger.LogInformation("Email sent successfully to {Recipients}", emailRequest.To);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send email to {Recipients}", emailRequest.To);
            return false;
        }
    }

    public async Task<List<EmailRequest>> GetPendingEmailsAsync()
    {
        var pendingEmails = new List<EmailRequest>();

        try
        {
            var queueFiles = Directory.GetFiles(_queueFolder, "*.json");
            
            foreach (var file in queueFiles)
            {
                try
                {
                    var json = await File.ReadAllTextAsync(file);
                    var emailRequest = JsonSerializer.Deserialize<EmailRequest>(json);
                    
                    if (emailRequest != null)
                    {
                        pendingEmails.Add(emailRequest);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Failed to deserialize email request from {File}", file);
                    // Move corrupted file to error folder
                    var errorFile = Path.Combine(_emailConfig.ErrorFolder, Path.GetFileName(file));
                    File.Move(file, errorFile);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to get pending emails");
        }

        return pendingEmails.OrderBy(e => e.Priority).ThenBy(e => e.RequestedAt).ToList();
    }

    public async Task ProcessEmailQueueAsync()
    {
        try
        {
            var pendingEmails = await GetPendingEmailsAsync();
            
            foreach (var emailRequest in pendingEmails)
            {
                var fileName = $"{emailRequest.RequestedAt:yyyyMMdd_HHmmss}_{Guid.NewGuid():N}.json";
                var queueFile = Path.Combine(_queueFolder, fileName);
                
                try
                {
                    var success = await SendEmailAsync(emailRequest);
                    
                    if (success)
                    {
                        // Move to processed folder
                        var processedFile = Path.Combine(_emailConfig.ProcessedFolder, fileName);
                        if (File.Exists(queueFile))
                        {
                            File.Move(queueFile, processedFile);
                        }
                        _logger.LogInformation("Email processed successfully: {Subject}", emailRequest.Subject);
                    }
                    else
                    {
                        // Move to error folder for retry later
                        var errorFile = Path.Combine(_emailConfig.ErrorFolder, fileName);
                        if (File.Exists(queueFile))
                        {
                            File.Move(queueFile, errorFile);
                        }
                        _logger.LogWarning("Email processing failed: {Subject}", emailRequest.Subject);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing email: {Subject}", emailRequest.Subject);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process email queue");
        }
    }

    public async Task QueueEmailAsync(EmailRequest emailRequest)
    {
        try
        {
            var fileName = $"{DateTime.Now:yyyyMMdd_HHmmss}_{Guid.NewGuid():N}.json";
            var filePath = Path.Combine(_queueFolder, fileName);
            
            var json = JsonSerializer.Serialize(emailRequest, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            
            await File.WriteAllTextAsync(filePath, json);
            _logger.LogInformation("Email queued successfully: {Subject}", emailRequest.Subject);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to queue email: {Subject}", emailRequest.Subject);
        }
    }
}

