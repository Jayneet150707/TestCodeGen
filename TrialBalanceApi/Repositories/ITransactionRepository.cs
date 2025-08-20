namespace TrialBalanceApi.Repositories
{
    public interface ITransactionRepository
    {
        Task<(decimal Debit, decimal Credit)> GetRcTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate, string? branch = null);
        Task<(decimal Debit, decimal Credit)> GetVfTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate, string? branch = null);
        Task<decimal> GetChqTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate);
        Task<decimal> GetFdTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate);
        Task<(decimal Interest, decimal Tds)> GetCdPostedTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate);
        Task<(decimal Amount, decimal Tds)> GetFdPayTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate);
        Task<(decimal Amount, decimal Tds)> GetFdDueTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate);
        Task<(decimal SmAmt, decimal SmIntt, decimal SmPrinc)> GetSmTransactionsAsync(DateTime fromDate, DateTime toDate, string accountType);
    }
}
