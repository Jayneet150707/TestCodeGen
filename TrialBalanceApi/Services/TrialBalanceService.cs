using TrialBalanceApi.Models;
using TrialBalanceApi.Repositories;

namespace TrialBalanceApi.Services
{
    public class TrialBalanceService : ITrialBalanceService
    {
        private readonly IAccountRepository _accountRepository;
        private readonly ITransactionRepository _transactionRepository;
        private readonly ILogger<TrialBalanceService> _logger;

        public TrialBalanceService(
            IAccountRepository accountRepository,
            ITransactionRepository transactionRepository,
            ILogger<TrialBalanceService> logger)
        {
            _accountRepository = accountRepository;
            _transactionRepository = transactionRepository;
            _logger = logger;
        }

        public async Task<TrialBalanceResponse> GenerateTrialBalanceAsync(TrialBalanceRequest request)
        {
            _logger.LogInformation("Generating trial balance for period {FromDate} to {ToDate}", 
                request.FromDate, request.ToDate);

            // Validate date range
            ValidateDateRange(request.FromDate, request.ToDate);

            // Get accounts
            var accounts = await _accountRepository.GetAccountsAsync(request.FromDate, request.AccountCode);
            
            // Get SM transactions once for all accounts (as per VB6 logic)
            var (smAmt, smIntt, smPrinc) = await _transactionRepository.GetSmTransactionsAsync(
                request.FromDate, request.ToDate, "C");
            var (smAmtLN, smInttLN, smPrincLN) = await _transactionRepository.GetSmTransactionsAsync(
                request.FromDate, request.ToDate, "LN");

            var accountBalances = new List<AccountBalance>();

            foreach (var account in accounts)
            {
                var balance = await CalculateAccountBalanceAsync(
                    account, request.FromDate, request.ToDate, request.Branch,
                    smAmt, smIntt, smPrinc, smAmtLN, smInttLN, smPrincLN);

                // Only include accounts with non-zero balances (as per VB6 logic)
                if (balance.DebitAmount != 0 || balance.CreditAmount != 0)
                {
                    accountBalances.Add(balance);
                }
            }

            return new TrialBalanceResponse
            {
                FromDate = request.FromDate,
                ToDate = request.ToDate,
                Branch = request.Branch,
                AccountBalances = accountBalances
            };
        }

        public async Task<IEnumerable<string>> GetAvailableBranchesAsync()
        {
            var branches = await _accountRepository.GetBranchesAsync();
            return new[] { "ALL" }.Concat(branches);
        }

        private async Task<AccountBalance> CalculateAccountBalanceAsync(
            Account account, DateTime fromDate, DateTime toDate, string? branch,
            decimal smAmt, decimal smIntt, decimal smPrinc,
            decimal smAmtLN, decimal smInttLN, decimal smPrincLN)
        {
            decimal debit = 0, credit = 0;

            // Start with opening balance
            if (account.YearOpeningBalance >= 0)
            {
                debit = account.YearOpeningBalance;
            }
            else
            {
                credit = -account.YearOpeningBalance;
            }

            // Add RC transactions
            var (rcDebit, rcCredit) = await _transactionRepository.GetRcTransactionsAsync(
                account.Code, fromDate, toDate, branch);
            debit += rcDebit;
            credit += rcCredit;

            // Add VF transactions
            var (vfDebit, vfCredit) = await _transactionRepository.GetVfTransactionsAsync(
                account.Code, fromDate, toDate, branch);
            debit += vfDebit;
            credit += vfCredit;

            // Handle CHQ transactions for specific account types
            (debit, credit) = await ProcessChqTransactions(account.Code, fromDate, toDate, debit, credit);

            // Handle FD transactions
            (debit, credit) = await ProcessFdTransactions(account.Code, fromDate, toDate, debit, credit);

            // Handle CDPOSTED transactions
            (debit, credit) = await ProcessCdPostedTransactions(account.Code, fromDate, toDate, debit, credit);

            // Handle FDPAY transactions
            (debit, credit) = await ProcessFdPayTransactions(account.Code, fromDate, toDate, debit, credit);

            // Handle FDDUE transactions
            (debit, credit) = await ProcessFdDueTransactions(account.Code, fromDate, toDate, debit, credit);

            // Handle SM-related accounts (HP/LN stock and money)
            (debit, credit) = ProcessSmTransactions(account.Code, debit, credit, 
                smAmt, smIntt, smPrinc, smAmtLN, smInttLN, smPrincLN);

            return new AccountBalance
            {
                AccountCode = account.Code,
                Description = account.Description,
                Lg = account.Lg,
                AType = account.AType,
                DebitAmount = debit > credit ? debit - credit : 0,
                CreditAmount = credit > debit ? credit - debit : 0,
                StartDate = fromDate,
                EndDate = toDate
            };
        }

        private async Task<(decimal debit, decimal credit)> ProcessChqTransactions(string accountCode, DateTime fromDate, DateTime toDate, 
            decimal debit, decimal credit)
        {
            var chqAccounts = new[] { "GACASH", "GASEILDE", "GACBIMTR", "GACBIALG", "GACENT", 
                "INHPMONY", "INLNINS", "GACBIDEL", "GAUTIBK", "GASBI" };

            if (chqAccounts.Contains(accountCode.ToUpper()))
            {
                var chqAmount = await _transactionRepository.GetChqTransactionsAsync(accountCode, fromDate, toDate);
                
                if (accountCode.ToUpper() == "INHPMONY" || accountCode.ToUpper() == "INLNINS")
                {
                    credit += chqAmount;
                }
                else
                {
                    debit += chqAmount;
                }
            }
            
            return (debit, credit);
        }

        private async Task<(decimal debit, decimal credit)> ProcessFdTransactions(string accountCode, DateTime fromDate, DateTime toDate, 
            decimal debit, decimal credit)
        {
            var fdAccounts = new[] { "GACASH", "GLFDRNWL", "GASEILDE", "DPFDPRN", "GLACUSTO", "GLLKSECU", "GLICDT" };
            
            // Check if account has bank_name (bank account)
            var accounts = await _accountRepository.GetAccountsAsync(fromDate, accountCode);
            var account = accounts.FirstOrDefault();
            bool isBankAccount = !string.IsNullOrEmpty(account?.BankName);

            if (isBankAccount || fdAccounts.Contains(accountCode.ToUpper()))
            {
                var fdAmount = await _transactionRepository.GetFdTransactionsAsync(accountCode, fromDate, toDate);
                
                if (isBankAccount || accountCode.ToUpper() == "GACASH" || 
                    accountCode.ToUpper() == "GLFDRNWL" || accountCode.ToUpper() == "GASEILDE")
                {
                    debit += fdAmount;
                }
                else if (accountCode.ToUpper() == "DPFDPRN" || accountCode.ToUpper() == "GLLKSECU")
                {
                    credit += fdAmount;
                }
            }
            
            return (debit, credit);
        }

        private async Task<(decimal debit, decimal credit)> ProcessCdPostedTransactions(string accountCode, DateTime fromDate, DateTime toDate, 
            decimal debit, decimal credit)
        {
            var cdPostedAccounts = new[] { "GEINTERP", "GLTDSPAY", "GLACCIFD", "GLACCADC", 
                "GLACCHPC", "GAAISECU", "GLACCICD", "GLACCLKS" };

            if (cdPostedAccounts.Contains(accountCode.ToUpper()))
            {
                var (interest, tds) = await _transactionRepository.GetCdPostedTransactionsAsync(
                    accountCode, fromDate, toDate);

                switch (accountCode.ToUpper())
                {
                    case "GEINTERP":
                        debit += interest;
                        break;
                    case "GLTDSPAY":
                        credit += tds;
                        break;
                    default:
                        credit += (interest - tds);
                        break;
                }
            }
            
            return (debit, credit);
        }

        private async Task<(decimal debit, decimal credit)> ProcessFdPayTransactions(string accountCode, DateTime fromDate, DateTime toDate, 
            decimal debit, decimal credit)
        {
            var (amount, tds) = await _transactionRepository.GetFdPayTransactionsAsync(accountCode, fromDate, toDate);
            
            // FDPAY affects multiple accounts differently
            debit += amount;
            credit += (amount - tds);

            // Special handling for GLTDSPAY
            if (accountCode.ToUpper() == "GLTDSPAY")
            {
                var (_, allTds) = await _transactionRepository.GetFdPayTransactionsAsync("", fromDate, toDate);
                credit += allTds;
            }
            
            return (debit, credit);
        }

        private async Task<(decimal debit, decimal credit)> ProcessFdDueTransactions(string accountCode, DateTime fromDate, DateTime toDate, 
            decimal debit, decimal credit)
        {
            var fdDueAccounts = new[] { "GEINTERP", "GLTDSPAY", "GLACCIFD" };

            if (fdDueAccounts.Contains(accountCode.ToUpper()))
            {
                var (amount, tds) = await _transactionRepository.GetFdDueTransactionsAsync(accountCode, fromDate, toDate);

                switch (accountCode.ToUpper())
                {
                    case "GEINTERP":
                        debit += amount;
                        break;
                    case "GLACCIFD":
                        credit += amount;
                        break;
                }
            }
            
            return (debit, credit);
        }

        private static (decimal debit, decimal credit) ProcessSmTransactions(string accountCode, decimal debit, decimal credit,
            decimal smAmt, decimal smIntt, decimal smPrinc,
            decimal smAmtLN, decimal smInttLN, decimal smPrincLN)
        {
            switch (accountCode.ToUpper())
            {
                case "INHPMONY":
                    debit += smIntt + smPrinc;
                    break;
                case "INLNINS":
                    debit += smInttLN + smPrincLN;
                    break;
                case "PLHIRER":
                    credit += smIntt;
                    break;
                case "PLBURROW":
                    credit += smInttLN;
                    break;
                case "PLHPSTCK":
                    credit += smPrinc;
                    break;
                case "PLLNSTCK":
                    credit += smPrincLN;
                    break;
            }
            
            return (debit, credit);
        }

        private static void ValidateDateRange(DateTime fromDate, DateTime toDate)
        {
            if (fromDate < new DateTime(1999, 4, 1))
            {
                throw new ArgumentException("Date should not be less than 01-04-99");
            }

            if (toDate < fromDate)
            {
                throw new ArgumentException("From Date must be less than or equal to To Date");
            }
        }
    }
}
