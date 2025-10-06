using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace FundamentoApiService;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly ApiService _apiService;
    private readonly TimeSpan _dailyExecutionTime = new TimeSpan(2, 0, 0); // 2:00 AM

    public Worker(ILogger<Worker> logger, ApiService apiService)
    {
        _logger = logger;
        _apiService = apiService;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Fundamento API Service started at: {time}", DateTimeOffset.Now);

        // Execute immediately on service start (optional - comment out if not needed)
        await ExecuteDailyTasks(stoppingToken);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var now = DateTime.Now;
                var nextRun = CalculateNextRunTime(now);
                var delay = nextRun - now;

                _logger.LogInformation("Next execution scheduled at: {nextRun}", nextRun);
                
                await Task.Delay(delay, stoppingToken);

                if (!stoppingToken.IsCancellationRequested)
                {
                    await ExecuteDailyTasks(stoppingToken);
                }
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("Service is stopping");
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in Worker execution");
                // Wait 1 hour before retrying in case of error
                await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
            }
        }
    }

    private async Task ExecuteDailyTasks(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Starting daily API calls at: {time}", DateTimeOffset.Now);

        try
        {
            await _apiService.ExecuteAllApiCalls(cancellationToken);
            _logger.LogInformation("Successfully completed all API calls at: {time}", DateTimeOffset.Now);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to execute daily API calls");
        }
    }

    private DateTime CalculateNextRunTime(DateTime currentTime)
    {
        var scheduledTime = currentTime.Date + _dailyExecutionTime;
        
        if (currentTime >= scheduledTime)
        {
            // If we've passed today's scheduled time, schedule for tomorrow
            scheduledTime = scheduledTime.AddDays(1);
        }

        return scheduledTime;
    }
}

