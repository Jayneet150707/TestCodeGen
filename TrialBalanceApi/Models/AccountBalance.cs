namespace TrialBalanceApi.Models
{
    public class AccountBalance
    {
        public string AccountCode { get; set; } = string.Empty;
        public string? Description { get; set; }
        public string? Lg { get; set; }
        public string? AType { get; set; }
        public decimal DebitAmount { get; set; }
        public decimal CreditAmount { get; set; }
        public decimal NetBalance => DebitAmount - CreditAmount;
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
    }
}
