-- Employee Management System Database Schema
-- Created with hierarchy and proper primary key identity management

-- =====================================================
-- 1. DEPARTMENT HIERARCHY TABLES
-- =====================================================

-- Main Departments Table
CREATE TABLE Departments (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentCode NVARCHAR(20) NOT NULL UNIQUE,
    DepartmentName NVARCHAR(100) NOT NULL,
    ParentDepartmentID INT NULL,
    IsActive BIT DEFAULT 1,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    ModifiedDate DATETIME2 DEFAULT GETDATE(),
    
    CONSTRAINT FK_Departments_Parent FOREIGN KEY (ParentDepartmentID) 
        REFERENCES Departments(DepartmentID)
);

-- Sub-Departments or Divisions
CREATE TABLE SubDepartments (
    SubDepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentID INT NOT NULL,
    SubDepartmentCode NVARCHAR(20) NOT NULL,
    SubDepartmentName NVARCHAR(100) NOT NULL,
    IsActive BIT DEFAULT 1,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    
    CONSTRAINT FK_SubDepartments_Department FOREIGN KEY (DepartmentID) 
        REFERENCES Departments(DepartmentID),
    CONSTRAINT UK_SubDepartments_Code UNIQUE (DepartmentID, SubDepartmentCode)
);

-- =====================================================
-- 2. EMPLOYEE CORE TABLES
-- =====================================================

-- Employee Status Master
CREATE TABLE EmployeeStatus (
    StatusID INT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    StatusName NVARCHAR(50) NOT NULL,
    Description NVARCHAR(200),
    IsActive BIT DEFAULT 1
);

-- Employee Types/Categories
CREATE TABLE EmployeeTypes (
    TypeID INT IDENTITY(1,1) PRIMARY KEY,
    TypeCode NVARCHAR(20) NOT NULL UNIQUE,
    TypeName NVARCHAR(50) NOT NULL,
    Description NVARCHAR(200),
    IsActive BIT DEFAULT 1
);

-- Main Employee Table
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeCode NVARCHAR(20) NOT NULL UNIQUE,
    FirstName NVARCHAR(50) NOT NULL,
    MiddleName NVARCHAR(50) NULL,
    LastName NVARCHAR(50) NOT NULL,
    FullName AS (FirstName + ' ' + ISNULL(MiddleName + ' ', '') + LastName) PERSISTED,
    
    -- Department Information
    DepartmentID INT NOT NULL,
    SubDepartmentID INT NULL,
    
    -- Employee Classification
    EmployeeTypeID INT NOT NULL,
    StatusID INT NOT NULL,
    
    -- Contact Information
    Email NVARCHAR(100) NULL,
    Phone NVARCHAR(20) NULL,
    
    -- Employment Details
    JoinDate DATE NOT NULL,
    TerminationDate DATE NULL,
    
    -- Audit Fields
    IsActive BIT DEFAULT 1,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(50) DEFAULT SYSTEM_USER,
    ModifiedDate DATETIME2 DEFAULT GETDATE(),
    ModifiedBy NVARCHAR(50) DEFAULT SYSTEM_USER,
    
    -- Foreign Key Constraints
    CONSTRAINT FK_Employees_Department FOREIGN KEY (DepartmentID) 
        REFERENCES Departments(DepartmentID),
    CONSTRAINT FK_Employees_SubDepartment FOREIGN KEY (SubDepartmentID) 
        REFERENCES SubDepartments(SubDepartmentID),
    CONSTRAINT FK_Employees_Type FOREIGN KEY (EmployeeTypeID) 
        REFERENCES EmployeeTypes(TypeID),
    CONSTRAINT FK_Employees_Status FOREIGN KEY (StatusID) 
        REFERENCES EmployeeStatus(StatusID)
);

-- =====================================================
-- 3. TARGET AND PERFORMANCE TABLES
-- =====================================================

-- Target Categories
CREATE TABLE TargetCategories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryCode NVARCHAR(20) NOT NULL UNIQUE,
    CategoryName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(200),
    IsActive BIT DEFAULT 1
);

-- Employee Targets
CREATE TABLE EmployeeTargets (
    TargetID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeID INT NOT NULL,
    CategoryID INT NOT NULL,
    TargetValue DECIMAL(18,2) NOT NULL,
    TargetPeriod NVARCHAR(20) NOT NULL, -- Monthly, Quarterly, Yearly
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    IsActive BIT DEFAULT 1,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    
    CONSTRAINT FK_EmployeeTargets_Employee FOREIGN KEY (EmployeeID) 
        REFERENCES Employees(EmployeeID),
    CONSTRAINT FK_EmployeeTargets_Category FOREIGN KEY (CategoryID) 
        REFERENCES TargetCategories(CategoryID)
);

-- =====================================================
-- 4. ADDITIONAL REFERENCE TABLES
-- =====================================================

-- Employee Roles/Positions
CREATE TABLE EmployeeRoles (
    RoleID INT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(20) NOT NULL UNIQUE,
    RoleName NVARCHAR(100) NOT NULL,
    DepartmentID INT NULL,
    Description NVARCHAR(200),
    IsActive BIT DEFAULT 1,
    
    CONSTRAINT FK_EmployeeRoles_Department FOREIGN KEY (DepartmentID) 
        REFERENCES Departments(DepartmentID)
);

-- Employee Role Assignments
CREATE TABLE EmployeeRoleAssignments (
    AssignmentID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeID INT NOT NULL,
    RoleID INT NOT NULL,
    AssignedDate DATE NOT NULL,
    UnassignedDate DATE NULL,
    IsActive BIT DEFAULT 1,
    
    CONSTRAINT FK_EmployeeRoleAssignments_Employee FOREIGN KEY (EmployeeID) 
        REFERENCES Employees(EmployeeID),
    CONSTRAINT FK_EmployeeRoleAssignments_Role FOREIGN KEY (RoleID) 
        REFERENCES EmployeeRoles(RoleID)
);

-- =====================================================
-- 5. INDEXES FOR PERFORMANCE
-- =====================================================

-- Department Indexes
CREATE INDEX IX_Departments_Code ON Departments(DepartmentCode);
CREATE INDEX IX_Departments_Parent ON Departments(ParentDepartmentID);

-- Employee Indexes
CREATE INDEX IX_Employees_Department ON Employees(DepartmentID);
CREATE INDEX IX_Employees_SubDepartment ON Employees(SubDepartmentID);
CREATE INDEX IX_Employees_Status ON Employees(StatusID);
CREATE INDEX IX_Employees_Type ON Employees(EmployeeTypeID);
CREATE INDEX IX_Employees_Code ON Employees(EmployeeCode);
CREATE INDEX IX_Employees_Name ON Employees(FirstName, LastName);
CREATE INDEX IX_Employees_Active ON Employees(IsActive);

-- Target Indexes
CREATE INDEX IX_EmployeeTargets_Employee ON EmployeeTargets(EmployeeID);
CREATE INDEX IX_EmployeeTargets_Period ON EmployeeTargets(TargetPeriod, StartDate, EndDate);

-- =====================================================
-- 6. TRIGGERS FOR AUDIT TRAIL
-- =====================================================

-- Update ModifiedDate trigger for Employees
CREATE TRIGGER TR_Employees_UpdateModified
ON Employees
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Employees 
    SET ModifiedDate = GETDATE(),
        ModifiedBy = SYSTEM_USER
    WHERE EmployeeID IN (SELECT EmployeeID FROM inserted);
END;

-- Update ModifiedDate trigger for Departments
CREATE TRIGGER TR_Departments_UpdateModified
ON Departments
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Departments 
    SET ModifiedDate = GETDATE()
    WHERE DepartmentID IN (SELECT DepartmentID FROM inserted);
END;
