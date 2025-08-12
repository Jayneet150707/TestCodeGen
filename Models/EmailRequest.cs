namespace EmailService.Models;

public class EmailRequest
{
    public string To { get; set; } = string.Empty;
    public string? Cc { get; set; }
    public string? Bcc { get; set; }
    public string Subject { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public bool IsHtml { get; set; } = false;
    public List<string> Attachments { get; set; } = new();
    public DateTime RequestedAt { get; set; } = DateTime.Now;
    public int Priority { get; set; } = 1; // 1 = High, 2 = Normal, 3 = Low
}

