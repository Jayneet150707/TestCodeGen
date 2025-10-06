using Microsoft.Extensions.Logging;
using System.Text;

namespace FundamentoApiService;

public class ApiService
{
    private readonly ILogger<ApiService> _logger;
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl = "https://sms.paisalo.in:979/PdlFundaMento/api/EMIDue";
    private readonly string _responseDirectory = "ApiResponses";

    public ApiService(ILogger<ApiService> logger, HttpClient httpClient)
    {
        _logger = logger;
        _httpClient = httpClient;
        
        // Create response directory if it doesn't exist
        if (!Directory.Exists(_responseDirectory))
        {
            Directory.CreateDirectory(_responseDirectory);
            _logger.LogInformation("Created response directory: {directory}", _responseDirectory);
        }
    }

    public async Task ExecuteAllApiCalls(CancellationToken cancellationToken)
    {
        var currentDate = DateTime.Now;
        var dateString = currentDate.ToString("dd-MMMM-yyyy");
        var previousDate = currentDate.AddDays(-1);
        var previousDateString = previousDate.ToString("dd-MMMM-yyyy");

        _logger.LogInformation("Executing API calls for date: {date}", dateString);

        // Pre Due API Calls
        await CallPreDueApi(0, dateString, cancellationToken);
        await CallPreDueApi(1, dateString, cancellationToken);
        await CallPreDueApi(3, dateString, cancellationToken);

        // Post Due API Calls
        await CallPostDueApi(2, dateString, cancellationToken);
        await CallPostDueApi(3, dateString, cancellationToken);
        await CallPostDueApi(4, dateString, cancellationToken);
        await CallPostDueApi(5, dateString, cancellationToken);

        // EMI Collected Data (previous day)
        await CallEmiCollectedApi(previousDate, previousDateString, cancellationToken);

        // Onboarding API Calls
        await CallOnboardingApi("ONBOARD", dateString, cancellationToken);
        await CallOnboardingApi("REJECT", dateString, cancellationToken);
        await CallOnboardingApi("SANCTION", dateString, cancellationToken);

        _logger.LogInformation("Completed all API calls for date: {date}", dateString);
    }

    private async Task CallPreDueApi(int dayToDue, string dateString, CancellationToken cancellationToken)
    {
        var url = $"{_baseUrl}/SendEMIPreDueData?dayToDue={dayToDue}";
        var fileName = $"Predue_response_{dayToDue}_{dateString}.txt";
        
        await CallApiAndSaveResponse(url, fileName, $"PreDue-{dayToDue}", cancellationToken);
    }

    private async Task CallPostDueApi(int dayRange, string dateString, CancellationToken cancellationToken)
    {
        var url = $"{_baseUrl}/SendEMIPreDueData?dayRange={dayRange}";
        var fileName = $"Postdue_response_{dayRange}_{dateString}.txt";
        
        await CallApiAndSaveResponse(url, fileName, $"PostDue-{dayRange}", cancellationToken);
    }

    private async Task CallEmiCollectedApi(DateTime inputDate, string dateString, CancellationToken cancellationToken)
    {
        var inputDateString = inputDate.ToString("yyyy-MM-dd");
        var url = $"{_baseUrl}/SendEMICollectedData?inputDate={inputDateString}";
        var fileName = $"EMI_response_{dateString}.txt";
        
        await CallApiAndSaveResponse(url, fileName, "EMI-Collected", cancellationToken);
    }

    private async Task CallOnboardingApi(string type, string dateString, CancellationToken cancellationToken)
    {
        var url = $"{_baseUrl}/SendOnboardingData?type={type}";
        var fileName = $"Onboard_response_{type}_{dateString}.txt";
        
        await CallApiAndSaveResponse(url, fileName, $"Onboarding-{type}", cancellationToken);
    }

    private async Task CallApiAndSaveResponse(string url, string fileName, string apiName, CancellationToken cancellationToken)
    {
        try
        {
            _logger.LogInformation("Calling API: {apiName} - {url}", apiName, url);
            
            var response = await _httpClient.GetAsync(url, cancellationToken);
            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            
            // Create file path
            var filePath = Path.Combine(_responseDirectory, fileName);
            
            // Prepare file content with metadata
            var fileContent = new StringBuilder();
            fileContent.AppendLine($"API: {apiName}");
            fileContent.AppendLine($"URL: {url}");
            fileContent.AppendLine($"Timestamp: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
            fileContent.AppendLine($"Status Code: {(int)response.StatusCode} ({response.StatusCode})");
            fileContent.AppendLine($"Success: {response.IsSuccessStatusCode}");
            fileContent.AppendLine(new string('-', 80));
            fileContent.AppendLine("Response:");
            fileContent.AppendLine(new string('-', 80));
            fileContent.AppendLine(content);
            
            // Save to file
            await File.WriteAllTextAsync(filePath, fileContent.ToString(), cancellationToken);
            
            if (response.IsSuccessStatusCode)
            {
                _logger.LogInformation("Successfully called {apiName} and saved response to {fileName}", apiName, fileName);
            }
            else
            {
                _logger.LogWarning("API {apiName} returned status code {statusCode}", apiName, response.StatusCode);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error calling API: {apiName} - {url}", apiName, url);
            
            // Save error to file
            var filePath = Path.Combine(_responseDirectory, fileName);
            var errorContent = new StringBuilder();
            errorContent.AppendLine($"API: {apiName}");
            errorContent.AppendLine($"URL: {url}");
            errorContent.AppendLine($"Timestamp: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
            errorContent.AppendLine($"ERROR: {ex.Message}");
            errorContent.AppendLine(new string('-', 80));
            errorContent.AppendLine("Stack Trace:");
            errorContent.AppendLine(ex.ToString());
            
            await File.WriteAllTextAsync(filePath, errorContent.ToString(), cancellationToken);
        }
    }
}

