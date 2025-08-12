using EmailService.Services;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace EmailService;

public class Program
{
    public static void Main(string[] args)
    {
        CreateHostBuilder(args).Build().Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .UseWindowsService(options =>
            {
                options.ServiceName = "Email Sending Service";
            })
            .ConfigureServices((hostContext, services) =>
            {
                services.AddHostedService<EmailWorkerService>();
                services.AddScoped<IEmailSender, EmailSender>();
                services.Configure<EmailConfiguration>(
                    hostContext.Configuration.GetSection("EmailConfiguration"));
            })
            .ConfigureLogging((context, logging) =>
            {
                logging.ClearProviders();
                logging.AddConsole();
                logging.AddEventLog();
            });
}

