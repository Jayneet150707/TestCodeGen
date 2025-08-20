namespace TrialBalanceApi.Models
{
    public class TrialBalanceResponse
    {
        public DateTime FromDate { get; set; }
        public DateTime ToDate { get; set; }
        public string? Branch { get; set; }
        public List<AccountBalance> AccountBalances { get; set; } = new();
        public decimal TotalDebits => AccountBalances.Sum(x => x.DebitAmount);
        public decimal TotalCredits => AccountBalances.Sum(x => x.CreditAmount);
        public bool IsBalanced => Math.Abs(TotalDebits - TotalCredits) < 0.01m;
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;
        public int TotalAccounts => AccountBalances.Count;
    }
}
