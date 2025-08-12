namespace EmailService.Models;

public class EmailConfiguration
{
    public string SmtpServer { get; set; } = string.Empty;
    public int SmtpPort { get; set; }
    public string SmtpUsername { get; set; } = string.Empty;
    public string SmtpPassword { get; set; } = string.Empty;
    public bool EnableSsl { get; set; }
    public string FromEmail { get; set; } = string.Empty;
    public string FromName { get; set; } = string.Empty;
    public int ProcessIntervalMinutes { get; set; } = 5;
    public string AttachmentFolder { get; set; } = string.Empty;
    public string ProcessedFolder { get; set; } = string.Empty;
    public string ErrorFolder { get; set; } = string.Empty;
}

