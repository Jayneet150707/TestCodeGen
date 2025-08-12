using EmailService.Models;
using EmailService.Utils;

namespace EmailService.Examples;

/// <summary>
/// Example console application showing how to queue emails for the service to process
/// </summary>
public class TestEmailSender
{
    public static async Task Main(string[] args)
    {
        Console.WriteLine("Email Service Test Application");
        Console.WriteLine("==============================");

        // Configuration - update these paths according to your setup
        var queueFolder = @"C:\EmailAttachments\Queue";
        var attachmentPath = @"C:\EmailAttachments\sample.pdf";

        try
        {
            // Example 1: Simple text email
            Console.WriteLine("1. Queuing simple text email...");
            var simpleEmail = new EmailRequest
            {
                To = "test@example.com",
                Subject = "Simple Test Email",
                Body = "This is a simple test email from the queue.",
                IsHtml = false,
                Priority = 2
            };

            var success1 = await EmailQueueHelper.QueueEmailAsync(queueFolder, simpleEmail);
            Console.WriteLine($"Simple email queued: {success1}");

            // Example 2: HTML email with attachment
            Console.WriteLine("\n2. Queuing HTML email with attachment...");
            var htmlEmail = new EmailRequest
            {
                To = "test@example.com",
                Cc = "cc@example.com",
                Subject = "HTML Email with Attachment",
                Body = @"
                    <html>
                    <body>
                        <h2>Test Email</h2>
                        <p>This is an <strong>HTML email</strong> with an attachment.</p>
                        <p>Please find the attached document.</p>
                        <br/>
                        <p>Best regards,<br/>Email Service</p>
                    </body>
                    </html>",
                IsHtml = true,
                Priority = 1,
                Attachments = File.Exists(attachmentPath) ? new List<string> { attachmentPath } : new List<string>()
            };

            var success2 = await EmailQueueHelper.QueueEmailAsync(queueFolder, htmlEmail);
            Console.WriteLine($"HTML email with attachment queued: {success2}");

            // Example 3: High priority email
            Console.WriteLine("\n3. Queuing high priority email...");
            var urgentEmail = new EmailRequest
            {
                To = "urgent@example.com",
                Subject = "URGENT: High Priority Email",
                Body = "This is a high priority email that should be processed first.",
                IsHtml = false,
                Priority = 1 // High priority
            };

            var success3 = await EmailQueueHelper.QueueEmailAsync(queueFolder, urgentEmail);
            Console.WriteLine($"High priority email queued: {success3}");

            Console.WriteLine("\nAll emails have been queued successfully!");
            Console.WriteLine("The Windows service will process them according to priority and timestamp.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }

        Console.WriteLine("\nPress any key to exit...");
        Console.ReadKey();
    }
}

