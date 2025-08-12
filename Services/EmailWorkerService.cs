using EmailService.Models;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace EmailService.Services;

public class EmailWorkerService : BackgroundService
{
    private readonly ILogger<EmailWorkerService> _logger;
    private readonly IServiceProvider _serviceProvider;
    private readonly EmailConfiguration _emailConfig;

    public EmailWorkerService(
        ILogger<EmailWorkerService> logger, 
        IServiceProvider serviceProvider,
        IOptions<EmailConfiguration> emailConfig)
    {
        _logger = logger;
        _serviceProvider = serviceProvider;
        _emailConfig = emailConfig.Value;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Email Worker Service started at: {time}", DateTimeOffset.Now);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                using var scope = _serviceProvider.CreateScope();
                var emailSender = scope.ServiceProvider.GetRequiredService<IEmailSender>();
                
                await emailSender.ProcessEmailQueueAsync();
                
                _logger.LogDebug("Email queue processed at: {time}", DateTimeOffset.Now);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred while processing email queue");
            }

            // Wait for the configured interval before processing again
            await Task.Delay(TimeSpan.FromMinutes(_emailConfig.ProcessIntervalMinutes), stoppingToken);
        }

        _logger.LogInformation("Email Worker Service stopped at: {time}", DateTimeOffset.Now);
    }

    public override async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Email Worker Service is starting");
        await base.StartAsync(cancellationToken);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Email Worker Service is stopping");
        await base.StopAsync(cancellationToken);
    }
}

