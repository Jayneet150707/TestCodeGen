using System.Data;

namespace TrialBalanceApi.Repositories
{
    public interface IBaseRepository
    {
        Task<T?> QuerySingleOrDefaultAsync<T>(string sql, object? parameters = null);
        Task<IEnumerable<T>> QueryAsync<T>(string sql, object? parameters = null);
        Task<int> ExecuteAsync(string sql, object? parameters = null);
    }
}
