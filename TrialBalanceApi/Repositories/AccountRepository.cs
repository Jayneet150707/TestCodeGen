using TrialBalanceApi.Data;
using TrialBalanceApi.Models;

namespace TrialBalanceApi.Repositories
{
    public class AccountRepository : BaseRepository, IAccountRepository
    {
        public AccountRepository(IDbConnectionFactory connectionFactory) : base(connectionFactory)
        {
        }

        public async Task<IEnumerable<Account>> GetAccountsAsync(DateTime fromDate, string? accountCode = null)
        {
            var sql = BuildAccountQuery(fromDate, accountCode);
            var parameters = new { AccountCode = accountCode, FromDate = fromDate };
            
            var accounts = await QueryAsync<dynamic>(sql, parameters);
            
            return accounts.Select(a => new Account
            {
                Code = a.code?.ToString() ?? string.Empty,
                Lg = a.lg?.ToString(),
                AType = a.atype?.ToString(),
                Description = a.desc?.ToString(),
                YearOpeningBalance = Convert.ToDecimal(a.yobal ?? 0),
                BankName = a.bank_name?.ToString()
            });
        }

        public async Task<IEnumerable<string>> GetBranchesAsync()
        {
            var sql = @"
                SELECT DISTINCT creator 
                FROM RTMGMTCREATOR 
                WHERE Access='Y' OR Creator=@Location
                ORDER BY creator";
            
            var parameters = new { Location = "AGRA" }; // Default location, should come from config
            
            var branches = await QueryAsync<string>(sql, parameters);
            return branches;
        }

        private static string BuildAccountQuery(DateTime fromDate, string? accountCode)
        {
            var baseQuery = @"
                SELECT lg, atype, code, [desc], bank_name, ";

            // Determine which year balance column to use based on financial year logic
            if (fromDate < new DateTime(2001, 4, 1))
            {
                baseQuery += "yobal as yobal";
            }
            else if (fromDate >= new DateTime(fromDate.Year, 4, 1) && fromDate < new DateTime(fromDate.Year + 1, 4, 1))
            {
                var yearSuffix = fromDate.Year.ToString().Substring(2, 2);
                baseQuery += $"yobal{yearSuffix} as yobal";
            }
            else
            {
                var yearSuffix = (fromDate.Year - 1).ToString().Substring(2, 2);
                baseQuery += $"yobal{yearSuffix} as yobal";
            }

            baseQuery += " FROM amast";

            if (!string.IsNullOrEmpty(accountCode))
            {
                baseQuery += " WHERE code = @AccountCode";
            }

            return baseQuery;
        }
    }
}
