using EmailService.Models;
using System.Text.Json;

namespace EmailService.Utils;

/// <summary>
/// Helper class for manually adding emails to the queue
/// This can be used by other applications to queue emails for processing
/// </summary>
public static class EmailQueueHelper
{
    /// <summary>
    /// Adds an email to the processing queue
    /// </summary>
    /// <param name="queueFolder">Path to the queue folder</param>
    /// <param name="emailRequest">Email request to queue</param>
    /// <returns>True if successfully queued, false otherwise</returns>
    public static async Task<bool> QueueEmailAsync(string queueFolder, EmailRequest emailRequest)
    {
        try
        {
            // Ensure queue directory exists
            Directory.CreateDirectory(queueFolder);
            
            var fileName = $"{DateTime.Now:yyyyMMdd_HHmmss}_{Guid.NewGuid():N}.json";
            var filePath = Path.Combine(queueFolder, fileName);
            
            var json = JsonSerializer.Serialize(emailRequest, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            
            await File.WriteAllTextAsync(filePath, json);
            return true;
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Creates a sample email request for testing
    /// </summary>
    /// <returns>Sample email request</returns>
    public static EmailRequest CreateSampleEmail()
    {
        return new EmailRequest
        {
            To = "recipient@example.com",
            Subject = "Test Email from Windows Service",
            Body = "This is a test email sent from the Windows Email Service.",
            IsHtml = false,
            Priority = 2,
            Attachments = new List<string>()
        };
    }

    /// <summary>
    /// Creates a sample email with HTML content and attachments
    /// </summary>
    /// <param name="attachmentPaths">List of attachment file paths</param>
    /// <returns>Sample HTML email request</returns>
    public static EmailRequest CreateSampleHtmlEmail(List<string> attachmentPaths)
    {
        return new EmailRequest
        {
            To = "recipient@example.com",
            Cc = "cc@example.com",
            Subject = "HTML Email with Attachments",
            Body = @"
                <html>
                <body>
                    <h2>Test HTML Email</h2>
                    <p>This is a <strong>test email</strong> with HTML formatting.</p>
                    <ul>
                        <li>Feature 1</li>
                        <li>Feature 2</li>
                        <li>Feature 3</li>
                    </ul>
                    <p>Best regards,<br/>Email Service</p>
                </body>
                </html>",
            IsHtml = true,
            Priority = 1,
            Attachments = attachmentPaths
        };
    }
}

