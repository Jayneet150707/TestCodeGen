-- Views and Stored Procedures for Employee Hierarchy Management
-- Provides easy access to hierarchical data with proper relationships

-- =====================================================
-- 1. VIEWS FOR EASY DATA ACCESS
-- =====================================================

-- Complete Employee Information View
CREATE VIEW vw_EmployeeDetails AS
SELECT 
    e.EmployeeID,
    e.EmployeeCode,
    e.FullName,
    e.FirstName,
    e.MiddleName,
    e.LastName,
    e.Email,
    e.Phone,
    e.JoinDate,
    e.TerminationDate,
    
    -- Department Information
    d.DepartmentCode,
    d.DepartmentName,
    sd.SubDepartmentCode,
    sd.SubDepartmentName,
    
    -- Employee Classification
    et.TypeCode AS EmployeeTypeCode,
    et.TypeName AS EmployeeTypeName,
    es.StatusCode AS EmployeeStatusCode,
    es.StatusName AS EmployeeStatusName,
    
    -- Current Role Information
    er.RoleCode AS CurrentRoleCode,
    er.RoleName AS CurrentRoleName,
    era.AssignedDate AS RoleAssignedDate,
    
    -- Status
    e.IsActive,
    e.CreatedDate,
    e.ModifiedDate
FROM Employees e
    INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
    LEFT JOIN SubDepartments sd ON e.SubDepartmentID = sd.SubDepartmentID
    INNER JOIN EmployeeTypes et ON e.EmployeeTypeID = et.TypeID
    INNER JOIN EmployeeStatus es ON e.StatusID = es.StatusID
    LEFT JOIN EmployeeRoleAssignments era ON e.EmployeeID = era.EmployeeID 
        AND era.IsActive = 1 AND era.UnassignedDate IS NULL
    LEFT JOIN EmployeeRoles er ON era.RoleID = er.RoleID
WHERE e.IsActive = 1;

-- Department Hierarchy View
CREATE VIEW vw_DepartmentHierarchy AS
WITH DepartmentCTE AS (
    -- Root departments
    SELECT 
        DepartmentID,
        DepartmentCode,
        DepartmentName,
        ParentDepartmentID,
        0 as Level,
        CAST(DepartmentName AS NVARCHAR(500)) as HierarchyPath,
        CAST(DepartmentCode AS NVARCHAR(100)) as HierarchyCode
    FROM Departments 
    WHERE ParentDepartmentID IS NULL
    
    UNION ALL
    
    -- Child departments
    SELECT 
        d.DepartmentID,
        d.DepartmentCode,
        d.DepartmentName,
        d.ParentDepartmentID,
        dc.Level + 1,
        CAST(dc.HierarchyPath + ' > ' + d.DepartmentName AS NVARCHAR(500)),
        CAST(dc.HierarchyCode + '.' + d.DepartmentCode AS NVARCHAR(100))
    FROM Departments d
        INNER JOIN DepartmentCTE dc ON d.ParentDepartmentID = dc.DepartmentID
)
SELECT 
    DepartmentID,
    DepartmentCode,
    DepartmentName,
    ParentDepartmentID,
    Level,
    HierarchyPath,
    HierarchyCode,
    (SELECT COUNT(*) FROM Employees WHERE DepartmentID = dc.DepartmentID AND IsActive = 1) as EmployeeCount
FROM DepartmentCTE dc;

-- Employee Targets Summary View
CREATE VIEW vw_EmployeeTargetsSummary AS
SELECT 
    e.EmployeeID,
    e.EmployeeCode,
    e.FullName,
    d.DepartmentName,
    tc.CategoryName as TargetCategory,
    et.TargetValue,
    et.TargetPeriod,
    et.StartDate,
    et.EndDate,
    CASE 
        WHEN et.EndDate < GETDATE() THEN 'Expired'
        WHEN et.StartDate > GETDATE() THEN 'Future'
        ELSE 'Active'
    END as TargetStatus
FROM EmployeeTargets et
    INNER JOIN Employees e ON et.EmployeeID = e.EmployeeID
    INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
    INNER JOIN TargetCategories tc ON et.CategoryID = tc.CategoryID
WHERE et.IsActive = 1 AND e.IsActive = 1;

-- Department Summary View
CREATE VIEW vw_DepartmentSummary AS
SELECT 
    d.DepartmentID,
    d.DepartmentCode,
    d.DepartmentName,
    COUNT(e.EmployeeID) as TotalEmployees,
    COUNT(CASE WHEN es.StatusCode = 'ACTIVE' THEN 1 END) as ActiveEmployees,
    COUNT(CASE WHEN et.TypeCode = 'FTE' THEN 1 END) as FullTimeEmployees,
    COUNT(CASE WHEN et.TypeCode = 'CONTRACT' THEN 1 END) as ContractEmployees,
    AVG(DATEDIFF(DAY, e.JoinDate, GETDATE())) as AvgTenureDays,
    MIN(e.JoinDate) as EarliestJoinDate,
    MAX(e.JoinDate) as LatestJoinDate
FROM Departments d
    LEFT JOIN Employees e ON d.DepartmentID = e.DepartmentID AND e.IsActive = 1
    LEFT JOIN EmployeeStatus es ON e.StatusID = es.StatusID
    LEFT JOIN EmployeeTypes et ON e.EmployeeTypeID = et.TypeID
WHERE d.IsActive = 1
GROUP BY d.DepartmentID, d.DepartmentCode, d.DepartmentName;

-- =====================================================
-- 2. STORED PROCEDURES
-- =====================================================

-- Get Employee Hierarchy by Department
CREATE PROCEDURE sp_GetEmployeesByDepartment
    @DepartmentCode NVARCHAR(20) = NULL,
    @IncludeSubDepartments BIT = 1
AS
BEGIN
    SET NOCOUNT ON;
    
    IF @DepartmentCode IS NULL
    BEGIN
        -- Return all employees
        SELECT * FROM vw_EmployeeDetails
        ORDER BY DepartmentName, SubDepartmentName, FullName;
    END
    ELSE
    BEGIN
        IF @IncludeSubDepartments = 1
        BEGIN
            -- Include sub-departments
            SELECT ed.* 
            FROM vw_EmployeeDetails ed
                INNER JOIN Departments d ON ed.DepartmentCode = d.DepartmentCode
            WHERE d.DepartmentCode = @DepartmentCode 
                OR d.ParentDepartmentID = (SELECT DepartmentID FROM Departments WHERE DepartmentCode = @DepartmentCode)
            ORDER BY ed.DepartmentName, ed.SubDepartmentName, ed.FullName;
        END
        ELSE
        BEGIN
            -- Only specific department
            SELECT * FROM vw_EmployeeDetails
            WHERE DepartmentCode = @DepartmentCode
            ORDER BY SubDepartmentName, FullName;
        END
    END
END;

-- Get Employee Target Performance
CREATE PROCEDURE sp_GetEmployeeTargets
    @EmployeeCode NVARCHAR(20) = NULL,
    @DepartmentCode NVARCHAR(20) = NULL,
    @TargetPeriod NVARCHAR(20) = NULL,
    @StartDate DATE = NULL,
    @EndDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ets.*,
        DATEDIFF(DAY, ets.StartDate, ISNULL(ets.EndDate, GETDATE())) as TargetDurationDays,
        CASE 
            WHEN ets.EndDate < GETDATE() THEN 'Completed'
            WHEN ets.StartDate > GETDATE() THEN 'Upcoming'
            ELSE 'In Progress'
        END as CurrentStatus
    FROM vw_EmployeeTargetsSummary ets
    WHERE (@EmployeeCode IS NULL OR ets.EmployeeCode = @EmployeeCode)
        AND (@DepartmentCode IS NULL OR ets.DepartmentName LIKE '%' + @DepartmentCode + '%')
        AND (@TargetPeriod IS NULL OR ets.TargetPeriod = @TargetPeriod)
        AND (@StartDate IS NULL OR ets.StartDate >= @StartDate)
        AND (@EndDate IS NULL OR ets.EndDate <= @EndDate)
    ORDER BY ets.EmployeeCode, ets.StartDate DESC;
END;

-- Add New Employee with Validation
CREATE PROCEDURE sp_AddEmployee
    @EmployeeCode NVARCHAR(20),
    @FirstName NVARCHAR(50),
    @MiddleName NVARCHAR(50) = NULL,
    @LastName NVARCHAR(50),
    @DepartmentCode NVARCHAR(20),
    @SubDepartmentCode NVARCHAR(20) = NULL,
    @EmployeeTypeCode NVARCHAR(20) = 'FTE',
    @Email NVARCHAR(100) = NULL,
    @Phone NVARCHAR(20) = NULL,
    @JoinDate DATE = NULL,
    @RoleCode NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Validate inputs
        IF EXISTS (SELECT 1 FROM Employees WHERE EmployeeCode = @EmployeeCode)
        BEGIN
            RAISERROR('Employee code already exists', 16, 1);
            RETURN;
        END
        
        DECLARE @DepartmentID INT, @SubDepartmentID INT, @EmployeeTypeID INT, @StatusID INT, @RoleID INT;
        
        -- Get Department ID
        SELECT @DepartmentID = DepartmentID FROM Departments WHERE DepartmentCode = @DepartmentCode;
        IF @DepartmentID IS NULL
        BEGIN
            RAISERROR('Invalid Department Code', 16, 1);
            RETURN;
        END
        
        -- Get Sub-Department ID if provided
        IF @SubDepartmentCode IS NOT NULL
        BEGIN
            SELECT @SubDepartmentID = SubDepartmentID 
            FROM SubDepartments 
            WHERE SubDepartmentCode = @SubDepartmentCode AND DepartmentID = @DepartmentID;
        END
        
        -- Get Employee Type ID
        SELECT @EmployeeTypeID = TypeID FROM EmployeeTypes WHERE TypeCode = @EmployeeTypeCode;
        IF @EmployeeTypeID IS NULL
        BEGIN
            RAISERROR('Invalid Employee Type Code', 16, 1);
            RETURN;
        END
        
        -- Get Active Status ID
        SELECT @StatusID = StatusID FROM EmployeeStatus WHERE StatusCode = 'ACTIVE';
        
        -- Set default join date
        IF @JoinDate IS NULL SET @JoinDate = GETDATE();
        
        -- Insert Employee
        DECLARE @NewEmployeeID INT;
        INSERT INTO Employees (
            EmployeeCode, FirstName, MiddleName, LastName,
            DepartmentID, SubDepartmentID, EmployeeTypeID, StatusID,
            Email, Phone, JoinDate
        ) VALUES (
            @EmployeeCode, @FirstName, @MiddleName, @LastName,
            @DepartmentID, @SubDepartmentID, @EmployeeTypeID, @StatusID,
            @Email, @Phone, @JoinDate
        );
        
        SET @NewEmployeeID = SCOPE_IDENTITY();
        
        -- Assign Role if provided
        IF @RoleCode IS NOT NULL
        BEGIN
            SELECT @RoleID = RoleID FROM EmployeeRoles WHERE RoleCode = @RoleCode;
            IF @RoleID IS NOT NULL
            BEGIN
                INSERT INTO EmployeeRoleAssignments (EmployeeID, RoleID, AssignedDate)
                VALUES (@NewEmployeeID, @RoleID, @JoinDate);
            END
        END
        
        COMMIT TRANSACTION;
        
        -- Return the new employee details
        SELECT * FROM vw_EmployeeDetails WHERE EmployeeID = @NewEmployeeID;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;

-- Get Department Statistics
CREATE PROCEDURE sp_GetDepartmentStatistics
    @DepartmentCode NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ds.*,
        CAST(ds.ActiveEmployees AS FLOAT) / NULLIF(ds.TotalEmployees, 0) * 100 as ActiveEmployeePercentage,
        CAST(ds.FullTimeEmployees AS FLOAT) / NULLIF(ds.TotalEmployees, 0) * 100 as FullTimePercentage,
        ds.AvgTenureDays / 365.0 as AvgTenureYears
    FROM vw_DepartmentSummary ds
    WHERE (@DepartmentCode IS NULL OR ds.DepartmentCode = @DepartmentCode)
    ORDER BY ds.TotalEmployees DESC;
END;
