using System.ComponentModel.DataAnnotations;

namespace TrialBalanceApi.Models
{
    public class TrialBalanceRequest
    {
        [Required]
        public DateTime FromDate { get; set; }
        
        [Required]
        public DateTime ToDate { get; set; }
        
        public string? Branch { get; set; } = "ALL";
        
        public string? AccountCode { get; set; }
    }
}
