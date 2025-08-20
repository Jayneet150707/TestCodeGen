# Trial Balance API

A .NET Core 8 Web API that converts VB6 trial balance functionality to modern C# with JSON output. This API generates trial balance reports from financial data without using Entity Framework or Dapper - using raw ADO.NET for database operations.

## Features

- **Trial Balance Generation**: Generate trial balance reports for specified date ranges
- **Branch Filtering**: Filter data by specific branches or view all branches
- **Account-Specific Reports**: Generate reports for specific account codes
- **Financial Year Logic**: Handles April 1st-based financial year calculations
- **Complex Business Rules**: Implements all VB6 business logic for different account types
- **JSON Output**: Clean JSON responses for easy integration
- **Swagger Documentation**: Built-in API documentation
- **Error Handling**: Comprehensive error handling with meaningful responses

## API Endpoints

### Generate Trial Balance

#### POST `/api/trialbalance/generate`
Generate trial balance using POST method with request body.

**Request Body:**
```json
{
  "fromDate": "2023-04-01",
  "toDate": "2024-03-31",
  "branch": "ALL",
  "accountCode": null
}
```

#### GET `/api/trialbalance`
Generate trial balance using GET method with query parameters.

**Query Parameters:**
- `fromDate` (required): Start date in yyyy-MM-dd format
- `toDate` (required): End date in yyyy-MM-dd format
- `branch` (optional): Branch code, defaults to "ALL"
- `accountCode` (optional): Specific account code to filter

**Example:**
```
GET /api/trialbalance?fromDate=2023-04-01&toDate=2024-03-31&branch=ALL
```

### Get Available Branches

#### GET `/api/trialbalance/branches`
Returns list of available branch codes for filtering.

### Health Check

#### GET `/api/trialbalance/health`
Returns API health status.

## Response Format

### Trial Balance Response
```json
{
  "fromDate": "2023-04-01T00:00:00",
  "toDate": "2024-03-31T00:00:00",
  "branch": "ALL",
  "accountBalances": [
    {
      "accountCode": "GACASH",
      "description": "Cash Account",
      "lg": "A",
      "aType": "ASSET",
      "debitAmount": 150000.00,
      "creditAmount": 0.00,
      "netBalance": 150000.00,
      "startDate": "2023-04-01T00:00:00",
      "endDate": "2024-03-31T00:00:00"
    }
  ],
  "totalDebits": 150000.00,
  "totalCredits": 150000.00,
  "isBalanced": true,
  "generatedAt": "2024-01-15T10:30:00Z",
  "totalAccounts": 1
}
```

### Error Response
```json
{
  "message": "Date should not be less than 01-04-99",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "traceId": "0HN7GLLMTC4SV:00000001"
}
```

## Database Tables

The API works with the following database tables:

- **amast**: Account master data with opening balances
- **rc**: Receipt transactions
- **vf**: Voucher transactions  
- **chq**: Cheque transactions
- **fd**: Fixed deposit transactions
- **cdposted**: Posted certificate of deposit data
- **fdpay**: Fixed deposit payment transactions
- **fddue**: Fixed deposit due transactions
- **sm**: Scheme master data
- **rtmgmtcreator**: Branch/creator management

## Configuration

### Database Connection

Update the connection string in `appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=SERVER_NAME;Database=DATABASE_NAME;Trusted_Connection=true;TrustServerCertificate=true;"
  }
}
```

For SQL Server Authentication:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=SERVER_NAME;Database=DATABASE_NAME;User Id=USERNAME;Password=PASSWORD_HERE;TrustServerCertificate=true;"
  }
}
```

## Setup Instructions

### Prerequisites
- .NET 8.0 SDK
- SQL Server (or compatible database)
- Visual Studio 2022 or VS Code

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TrialBalanceApi
   ```

2. **Restore packages**
   ```bash
   dotnet restore
   ```

3. **Update connection string**
   - Edit `appsettings.json` and `appsettings.Development.json`
   - Set your database connection string

4. **Run the application**
   ```bash
   dotnet run
   ```

5. **Access Swagger UI**
   - Navigate to `https://localhost:5001` (or the port shown in console)
   - Swagger UI will be displayed at the root URL

## Business Logic

The API implements complex financial business logic from the original VB6 system:

### Account Types
- **Cash Accounts**: GACASH, GASEILDE, etc.
- **Bank Accounts**: Accounts with bank_name field
- **Interest Accounts**: GEINTERP, GLACCIFD, etc.
- **TDS Accounts**: GLTDSPAY
- **HP/LN Accounts**: INHPMONY, INLNINS, PLHIRER, etc.

### Financial Year Logic
- Financial year starts April 1st
- Automatically selects appropriate year balance columns (yobal, yobal01, yobal02, etc.)
- Handles date validation (minimum date: April 1, 1999)

### Transaction Processing
- **RC Transactions**: Receipt entries with branch filtering
- **VF Transactions**: Voucher entries with location filtering
- **CHQ Transactions**: Cheque transactions for specific account types
- **FD Transactions**: Fixed deposit investments and maturities
- **CDPOSTED**: Interest and TDS calculations
- **FDPAY/FDDUE**: Payment and due amount processing
- **SM Transactions**: Scheme-related calculations for HP/LN accounts

## Architecture

### Layered Architecture
- **Controllers**: API endpoints and request/response handling
- **Services**: Business logic and orchestration
- **Repositories**: Data access layer with raw ADO.NET
- **Models**: Data transfer objects and entities
- **Middleware**: Error handling and cross-cutting concerns

### Dependency Injection
All services are registered with appropriate lifetimes:
- **Scoped**: Database connections, repositories, services
- **Singleton**: Configuration, logging

### Error Handling
- Global exception middleware
- Structured error responses
- Comprehensive logging
- Request tracing

## Performance Considerations

- **Connection Management**: Proper disposal of database connections
- **Query Optimization**: Efficient SQL queries with appropriate indexes
- **Memory Management**: Streaming large result sets
- **Caching**: Consider implementing caching for frequently accessed data

## Security

- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: Model validation attributes
- **Error Information**: Sanitized error messages in production
- **Connection Security**: Encrypted connections with TrustServerCertificate

## Testing

### Manual Testing
Use Swagger UI for interactive testing:
1. Navigate to the root URL when running in development
2. Use the "Try it out" feature for each endpoint
3. Test with various date ranges and branch filters

### Sample Requests

**Basic Trial Balance:**
```bash
curl -X GET "https://localhost:5001/api/trialbalance?fromDate=2023-04-01&toDate=2024-03-31"
```

**Branch-Specific Trial Balance:**
```bash
curl -X GET "https://localhost:5001/api/trialbalance?fromDate=2023-04-01&toDate=2024-03-31&branch=DELHI"
```

**Account-Specific Trial Balance:**
```bash
curl -X GET "https://localhost:5001/api/trialbalance?fromDate=2023-04-01&toDate=2024-03-31&accountCode=GACASH"
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify connection string
   - Check SQL Server service status
   - Ensure database exists and user has permissions

2. **Date Validation Errors**
   - Ensure dates are in yyyy-MM-dd format
   - From date must be >= April 1, 1999
   - To date must be >= From date

3. **No Data Returned**
   - Check if accounts exist in amast table
   - Verify transaction data in respective tables
   - Ensure date range contains data

### Logging
The application logs to console and debug output. Check logs for detailed error information.

## Migration from VB6

This API faithfully reproduces the VB6 trial balance logic:

### Key Differences
- **Async Operations**: All database operations are asynchronous
- **JSON Output**: Instead of Crystal Reports
- **REST API**: Instead of desktop application
- **Dependency Injection**: Modern IoC container
- **Structured Logging**: Instead of MsgBox debugging

### Preserved Logic
- All account type-specific calculations
- Financial year handling
- Branch filtering logic
- Transaction aggregation rules
- Date validation rules

## Contributing

1. Follow existing code patterns
2. Add unit tests for new features
3. Update documentation
4. Ensure all business logic matches VB6 behavior

## License

[Add your license information here]
