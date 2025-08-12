using EmailService.Models;

namespace EmailService.Services;

public interface IEmailSender
{
    Task<bool> SendEmailAsync(EmailRequest emailRequest);
    Task<List<EmailRequest>> GetPendingEmailsAsync();
    Task ProcessEmailQueueAsync();
}

