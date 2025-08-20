using TrialBalanceApi.Data;

namespace TrialBalanceApi.Repositories
{
    public class TransactionRepository : BaseRepository, ITransactionRepository
    {
        public TransactionRepository(IDbConnectionFactory connectionFactory) : base(connectionFactory)
        {
        }

        public async Task<(decimal Debit, decimal Credit)> GetRcTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate, string? branch = null)
        {
            var sql = @"
                SELECT ISNULL(SUM(dr), 0) as Debit, ISNULL(SUM(cr), 0) as Credit 
                FROM RC 
                WHERE ahead = @AccountCode 
                AND vdate >= @FromDate 
                AND vdate <= @ToDate";

            if (!string.IsNullOrEmpty(branch) && branch != "ALL")
            {
                sql += " AND (branch_cd = @BranchCode OR location = @Branch)";
            }

            var parameters = new 
            { 
                AccountCode = accountCode, 
                FromDate = fromDate, 
                ToDate = toDate,
                BranchCode = branch?.Substring(0, 1),
                Branch = branch?.ToUpper()
            };

            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (Convert.ToDecimal(result?.Debit ?? 0), Convert.ToDecimal(result?.Credit ?? 0));
        }

        public async Task<(decimal Debit, decimal Credit)> GetVfTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate, string? branch = null)
        {
            var sql = @"
                SELECT ISNULL(SUM(dr), 0) as Debit, ISNULL(SUM(cr), 0) as Credit 
                FROM VF 
                WHERE ahead = @AccountCode 
                AND vdate >= @FromDate 
                AND vdate <= @ToDate";

            if (!string.IsNullOrEmpty(branch) && branch != "ALL")
            {
                sql += " AND (linkno = @Branch OR location = @Branch)";
            }

            var parameters = new 
            { 
                AccountCode = accountCode, 
                FromDate = fromDate, 
                ToDate = toDate,
                Branch = branch?.ToUpper()
            };

            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (Convert.ToDecimal(result?.Debit ?? 0), Convert.ToDecimal(result?.Credit ?? 0));
        }

        public async Task<decimal> GetChqTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate)
        {
            var sql = @"
                SELECT ISNULL(SUM(amt), 0) as Amount 
                FROM CHQ 
                WHERE org_rcp_dt >= @FromDate 
                AND org_rcp_dt <= @ToDate 
                AND (drcode = @AccountCode OR crcode = @AccountCode)";

            var parameters = new { AccountCode = accountCode, FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<decimal>(sql, parameters);
            return result;
        }

        public async Task<decimal> GetFdTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate)
        {
            var sql = BuildFdQuery(accountCode);
            var parameters = new { AccountCode = accountCode, FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<decimal>(sql, parameters);
            return result;
        }

        public async Task<(decimal Interest, decimal Tds)> GetCdPostedTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate)
        {
            var sql = BuildCdPostedQuery(accountCode);
            var parameters = new { FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (Convert.ToDecimal(result?.Interest ?? 0), Convert.ToDecimal(result?.Tds ?? 0));
        }

        public async Task<(decimal Amount, decimal Tds)> GetFdPayTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate)
        {
            var sql = @"
                SELECT ISNULL(SUM(amt), 0) as Amount, ISNULL(SUM(tds_amt), 0) as Tds 
                FROM FDPAY 
                WHERE date >= @FromDate 
                AND date <= @ToDate 
                AND (drcode = @AccountCode OR crcode = @AccountCode)";

            var parameters = new { AccountCode = accountCode, FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (Convert.ToDecimal(result?.Amount ?? 0), Convert.ToDecimal(result?.Tds ?? 0));
        }

        public async Task<(decimal Amount, decimal Tds)> GetFdDueTransactionsAsync(string accountCode, DateTime fromDate, DateTime toDate)
        {
            var sql = @"
                SELECT ISNULL(SUM(amt), 0) as Amount, ISNULL(SUM(tds_amt), 0) as Tds 
                FROM FDDUE 
                WHERE date >= @FromDate 
                AND date <= @ToDate";

            var parameters = new { FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (Convert.ToDecimal(result?.Amount ?? 0), Convert.ToDecimal(result?.Tds ?? 0));
        }

        public async Task<(decimal SmAmt, decimal SmIntt, decimal SmPrinc)> GetSmTransactionsAsync(DateTime fromDate, DateTime toDate, string accountType)
        {
            var leftCondition = accountType == "C" ? "IN ('C')" : "NOT IN ('C')";
            
            var sql = $@"
                SELECT 
                    ISNULL(SUM(a.amt), 0) as SmAmt,
                    ISNULL(SUM(a.inst_intt), 0) as SmIntt,
                    ISNULL(SUM(a.inst_princ), 0) as SmPrinc
                FROM CHQ a 
                INNER JOIN SM b ON b.code = a.code
                WHERE a.ins_due_dt >= @FromDate 
                AND a.ins_due_dt <= @ToDate
                AND (a.ins_due_dt < b.comp_dt OR b.comp_dt IS NULL)
                AND LEFT(b.CODE, 1) {leftCondition}";

            var parameters = new { FromDate = fromDate, ToDate = toDate };
            var result = await QuerySingleOrDefaultAsync<dynamic>(sql, parameters);
            return (
                Convert.ToDecimal(result?.SmAmt ?? 0),
                Convert.ToDecimal(result?.SmIntt ?? 0),
                Convert.ToDecimal(result?.SmPrinc ?? 0)
            );
        }

        private static string BuildFdQuery(string accountCode)
        {
            return accountCode.ToUpper() switch
            {
                "GACASH" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) <> 'AC' AND pay_mode = 'C'",
                
                "GLFDRNWL" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) <> 'AC' AND pay_mode = 'R'",
                
                "GASEILDE" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) <> 'AC' AND pay_mode IS NULL",
                
                "DPFDPRN" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 1) = 'D'",
                
                "GLACUSTO" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) = 'AA'",
                
                "GLLKSECU" => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) = 'LK'",
                
                _ => @"
                    SELECT ISNULL(SUM(invest), 0) 
                    FROM FD 
                    WHERE date >= @FromDate AND date <= @ToDate 
                    AND LEFT(code, 2) <> 'AC' AND pay_mode = 'B' AND bank_code = @AccountCode"
            };
        }

        private static string BuildCdPostedQuery(string accountCode)
        {
            return accountCode.ToUpper() switch
            {
                "GEINTERP" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, 0 as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate",
                
                "GLTDSPAY" => @"
                    SELECT 0 as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate",
                
                "GLACCIFD" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 1)) = 'D'",
                
                "GLACCADC" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 2)) = 'AA'",
                
                "GAAISECU" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 2)) = 'MF'",
                
                "GLACCHPC" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 2)) = 'AC'",
                
                "GLACCICD" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 1)) = 'I'",
                
                "GLACCLKS" => @"
                    SELECT ISNULL(SUM(intt), 0) as Interest, ISNULL(SUM(tds), 0) as Tds 
                    FROM CDPOSTED 
                    WHERE cumm_dt >= @FromDate AND cumm_dt <= @ToDate 
                    AND UPPER(LEFT(code, 2)) = 'LK'",
                
                _ => "SELECT 0 as Interest, 0 as Tds"
            };
        }
    }
}
