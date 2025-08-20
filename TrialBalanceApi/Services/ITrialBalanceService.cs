using TrialBalanceApi.Models;

namespace TrialBalanceApi.Services
{
    public interface ITrialBalanceService
    {
        Task<TrialBalanceResponse> GenerateTrialBalanceAsync(TrialBalanceRequest request);
        Task<IEnumerable<string>> GetAvailableBranchesAsync();
    }
}
