-- Simple Employee Table Schema
-- Based exactly on the Excel spreadsheet structure provided

-- =====================================================
-- SIMPLE EMPLOYEE TABLE - MATCHES EXCEL STRUCTURE
-- =====================================================

CREATE TABLE Employees (
    -- Primary Key with Identity
    ID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Excel Column Mappings (based on visible columns in image)
    EmployeeID NVARCHAR(20) NOT NULL UNIQUE,
    DepartmentVertical NVARCHAR(50),
    Names NVARCHAR(100),
    Target NVARCHAR(50),
    L1Name NVARCHAR(100),
    L1EmployeeCode NVARCHAR(20),
    L2Name NVARCHAR(100),
    L2EmployeeID NVARCHAR(20),
    L3Name NVARCHAR(100),
    L3EmployeeID NVARCHAR(20),
    L4Name NVARCHAR(100),
    L4EmployeeID NVARCHAR(20),
    L5Name NVARCHAR(100),
    L5EmployeeID NVARCHAR(20),
    L6Name NVARCHAR(100),
    L6EmployeeID NVARCHAR(20),
    L7Name NVARCHAR(100),
    L7EmployeeID NVARCHAR(20),
    L8Name NVARCHAR(100),
    L8EmployeeID NVARCHAR(20),
    L9Name NVARCHAR(100),
    L9EmployeeID NVARCHAR(20),
    L10Name NVARCHAR(100),
    L10EmployeeID NVARCHAR(20),
    L11Name NVARCHAR(100),
    L11EmployeeID NVARCHAR(20),
    L12Name NVARCHAR(100),
    L12EmployeeID NVARCHAR(20),
    L13Name NVARCHAR(100),
    L13EmployeeID NVARCHAR(20),
    L14Name NVARCHAR(100),
    L14EmployeeID NVARCHAR(20),
    L15Name NVARCHAR(100),
    L15EmployeeID NVARCHAR(20),
    L16Name NVARCHAR(100),
    L16EmployeeID NVARCHAR(20),
    L17Name NVARCHAR(100),
    L17EmployeeID NVARCHAR(20),
    
    -- Audit fields (minimal)
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    ModifiedDate DATETIME2 DEFAULT GETDATE()
);

-- Index for performance on EmployeeID
CREATE INDEX IX_Employees_EmployeeID ON Employees(EmployeeID);
CREATE INDEX IX_Employees_DepartmentVertical ON Employees(DepartmentVertical);

-- Simple trigger for ModifiedDate
CREATE TRIGGER TR_Employees_UpdateModified
ON Employees
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Employees 
    SET ModifiedDate = GETDATE()
    WHERE ID IN (SELECT ID FROM inserted);
END;
