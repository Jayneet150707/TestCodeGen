using TrialBalanceApi.Models;

namespace TrialBalanceApi.Repositories
{
    public interface IAccountRepository
    {
        Task<IEnumerable<Account>> GetAccountsAsync(DateTime fromDate, string? accountCode = null);
        Task<IEnumerable<string>> GetBranchesAsync();
    }
}
