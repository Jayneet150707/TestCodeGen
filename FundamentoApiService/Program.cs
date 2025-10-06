using FundamentoApiService;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .WriteTo.Console()
    .WriteTo.File("logs/fundamento-service-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

try
{
    Log.Information("Starting Fundamento API Service");

    var builder = Host.CreateApplicationBuilder(args);

    // Add Windows Service support
    builder.Services.AddWindowsService(options =>
    {
        options.ServiceName = "Fundamento API Service";
    });

    // Add Serilog
    builder.Services.AddSerilog();

    // Add HttpClient
    builder.Services.AddHttpClient<ApiService>(client =>
    {
        client.Timeout = TimeSpan.FromMinutes(10);
    });

    // Add Worker Service
    builder.Services.AddHostedService<Worker>();

    var host = builder.Build();
    await host.RunAsync();

    Log.Information("Fundamento API Service stopped");
}
catch (Exception ex)
{
    Log.Fatal(ex, "Fundamento API Service terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}

