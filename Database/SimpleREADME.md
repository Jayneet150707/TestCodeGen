# Simple Employee Table Schema

This is a straightforward database table that exactly matches your Excel spreadsheet structure - no complex hierarchy, just a simple table to store your employee records as they are.

## 📋 Table Structure

**Single Table: `Employees`**
- `ID` - Primary key with identity (auto-increment)
- `EmployeeID` - Your employee ID from Excel (unique)
- `DepartmentVertical` - Department name
- `Names` - Employee status/name
- `Target` - Target value
- `L1Name` to `L17Name` - Level 1 to 17 names
- `L1EmployeeCode` to `L17EmployeeID` - Level 1 to 17 employee codes/IDs
- `CreatedDate` - When record was created
- `ModifiedDate` - When record was last updated

## 🚀 Usage

### Insert Data
```sql
INSERT INTO Employees (EmployeeID, DepartmentVertical, Names, Target, L1Name, L1EmployeeCode, ...)
VALUES ('AGR000001', 'AGRICULTURE', 'ACTIVE', '4000000', 'KAMLAJYOTI', 'PGL000000', ...);
```

### Query Data
```sql
-- Get all employees
SELECT * FROM Employees;

-- Get employees by department
SELECT * FROM Employees WHERE DepartmentVertical = 'AGRICULTURE';

-- Get employees by target range
SELECT * FROM Employees WHERE CAST(Target AS INT) > 1000000;
```

### Update Data
```sql
UPDATE Employees 
SET Target = '5000000' 
WHERE EmployeeID = 'AGR000001';
```

## 📊 Features

✅ **Simple Structure** - One table, matches your Excel exactly  
✅ **Identity Primary Key** - Auto-incrementing ID  
✅ **Unique Employee ID** - Prevents duplicate employee records  
✅ **Basic Indexing** - Fast searches on EmployeeID and Department  
✅ **Auto Timestamps** - Tracks when records are created/modified  

## 🔧 Installation

1. Run `SimpleEmployeeSchema.sql` to create the table
2. Run `SimpleEmployeeData.sql` to insert sample data
3. Start using the table immediately!

That's it - no complex setup, no multiple tables, just a simple table that stores your Excel data exactly as it is.
