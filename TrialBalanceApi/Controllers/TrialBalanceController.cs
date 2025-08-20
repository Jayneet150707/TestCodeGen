using Microsoft.AspNetCore.Mvc;
using TrialBalanceApi.Models;
using TrialBalanceApi.Services;

namespace TrialBalanceApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TrialBalanceController : ControllerBase
    {
        private readonly ITrialBalanceService _trialBalanceService;
        private readonly ILogger<TrialBalanceController> _logger;

        public TrialBalanceController(
            ITrialBalanceService trialBalanceService,
            ILogger<TrialBalanceController> logger)
        {
            _trialBalanceService = trialBalanceService;
            _logger = logger;
        }

        /// <summary>
        /// Generate trial balance for the specified date range and branch
        /// </summary>
        /// <param name="request">Trial balance request parameters</param>
        /// <returns>Trial balance data in JSON format</returns>
        [HttpPost("generate")]
        public async Task<ActionResult<TrialBalanceResponse>> GenerateTrialBalance([FromBody] TrialBalanceRequest request)
        {
            try
            {
                _logger.LogInformation("Received trial balance request for {FromDate} to {ToDate}, Branch: {Branch}", 
                    request.FromDate, request.ToDate, request.Branch);

                if (!ModelState.IsValid)
                {
                    return BadRequest(ModelState);
                }

                var result = await _trialBalanceService.GenerateTrialBalanceAsync(request);
                
                _logger.LogInformation("Trial balance generated successfully with {AccountCount} accounts", 
                    result.TotalAccounts);

                return Ok(result);
            }
            catch (ArgumentException ex)
            {
                _logger.LogWarning("Invalid request parameters: {Message}", ex.Message);
                return BadRequest(new ErrorResponse 
                { 
                    Message = ex.Message,
                    TraceId = HttpContext.TraceIdentifier
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating trial balance");
                return StatusCode(500, new ErrorResponse 
                { 
                    Message = "An error occurred while generating the trial balance",
                    Details = ex.Message,
                    TraceId = HttpContext.TraceIdentifier
                });
            }
        }

        /// <summary>
        /// Get trial balance for the specified date range and branch using GET method
        /// </summary>
        /// <param name="fromDate">Start date (yyyy-MM-dd)</param>
        /// <param name="toDate">End date (yyyy-MM-dd)</param>
        /// <param name="branch">Branch code (optional, defaults to ALL)</param>
        /// <param name="accountCode">Specific account code (optional)</param>
        /// <returns>Trial balance data in JSON format</returns>
        [HttpGet]
        public async Task<ActionResult<TrialBalanceResponse>> GetTrialBalance(
            [FromQuery] DateTime fromDate,
            [FromQuery] DateTime toDate,
            [FromQuery] string? branch = "ALL",
            [FromQuery] string? accountCode = null)
        {
            var request = new TrialBalanceRequest
            {
                FromDate = fromDate,
                ToDate = toDate,
                Branch = branch,
                AccountCode = accountCode
            };

            return await GenerateTrialBalance(request);
        }

        /// <summary>
        /// Get available branches for filtering
        /// </summary>
        /// <returns>List of available branch codes</returns>
        [HttpGet("branches")]
        public async Task<ActionResult<IEnumerable<string>>> GetBranches()
        {
            try
            {
                var branches = await _trialBalanceService.GetAvailableBranchesAsync();
                return Ok(branches);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving branches");
                return StatusCode(500, new ErrorResponse 
                { 
                    Message = "An error occurred while retrieving branches",
                    Details = ex.Message,
                    TraceId = HttpContext.TraceIdentifier
                });
            }
        }

        /// <summary>
        /// Health check endpoint
        /// </summary>
        /// <returns>API status</returns>
        [HttpGet("health")]
        public IActionResult Health()
        {
            return Ok(new { Status = "Healthy", Timestamp = DateTime.UtcNow });
        }
    }
}
