namespace TrialBalanceApi.Models
{
    public class Account
    {
        public string Code { get; set; } = string.Empty;
        public string? Lg { get; set; }
        public string? AType { get; set; }
        public string? Description { get; set; }
        public decimal YearOpeningBalance { get; set; }
        public string? BankName { get; set; }
    }
}
