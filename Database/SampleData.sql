-- Sample Data Insertion Script
-- Based on the employee data structure from the provided image

-- =====================================================
-- 1. INSERT MASTER DATA
-- =====================================================

-- Insert Employee Status
INSERT INTO EmployeeStatus (StatusCode, StatusName, Description) VALUES
('ACTIVE', 'Active', 'Currently employed and active'),
('INACTIVE', 'Inactive', 'Temporarily inactive'),
('TERMINATED', 'Terminated', 'Employment terminated');

-- Insert Employee Types
INSERT INTO EmployeeTypes (TypeCode, TypeName, Description) VALUES
('FTE', 'Full Time Employee', 'Regular full-time employee'),
('PTE', 'Part Time Employee', 'Part-time employee'),
('CONTRACT', 'Contract Employee', 'Contract-based employee'),
('INTERN', 'Intern', 'Internship position');

-- Insert Departments (Based on the data visible in the image)
INSERT INTO Departments (DepartmentCode, DepartmentName, ParentDepartmentID) VALUES
('AGRI', 'Agriculture', NULL),
('SALES', 'Sales', NULL),
('MARKETING', 'Marketing', NULL),
('FINANCE', 'Finance', NULL),
('HR', 'Human Resources', NULL),
('IT', 'Information Technology', NULL);

-- Insert Sub-Departments
INSERT INTO SubDepartments (DepartmentID, SubDepartmentCode, SubDepartmentName) VALUES
(1, 'AGRI-FIELD', 'Field Operations'),
(1, 'AGRI-PROC', 'Processing'),
(2, 'SALES-RETAIL', 'Retail Sales'),
(2, 'SALES-CORP', 'Corporate Sales'),
(3, 'MKT-DIGITAL', 'Digital Marketing'),
(3, 'MKT-TRAD', 'Traditional Marketing');

-- Insert Target Categories
INSERT INTO TargetCategories (CategoryCode, CategoryName, Description) VALUES
('SALES_TARGET', 'Sales Target', 'Monthly/Quarterly sales targets'),
('REVENUE_TARGET', 'Revenue Target', 'Revenue generation targets'),
('CUSTOMER_TARGET', 'Customer Acquisition', 'New customer acquisition targets'),
('RETENTION_TARGET', 'Customer Retention', 'Customer retention targets');

-- Insert Employee Roles
INSERT INTO EmployeeRoles (RoleCode, RoleName, DepartmentID, Description) VALUES
('MGR', 'Manager', NULL, 'Department Manager'),
('EXEC', 'Executive', NULL, 'Senior Executive'),
('ASSOC', 'Associate', NULL, 'Associate Level'),
('ANALYST', 'Analyst', NULL, 'Data/Business Analyst'),
('COORD', 'Coordinator', NULL, 'Project Coordinator');

-- =====================================================
-- 2. INSERT SAMPLE EMPLOYEE DATA
-- =====================================================

-- Sample employees based on the visible data structure
INSERT INTO Employees (
    EmployeeCode, FirstName, MiddleName, LastName, 
    DepartmentID, SubDepartmentID, EmployeeTypeID, StatusID,
    Email, Phone, JoinDate
) VALUES
-- Agriculture Department Employees
('AGR000001', 'Rajesh', 'Kumar', 'Sharma', 1, 1, 1, 1, 'rajesh.sharma@company.com', '9876543210', '2023-01-15'),
('AGR000002', 'Priya', NULL, 'Patel', 1, 1, 1, 1, 'priya.patel@company.com', '9876543211', '2023-02-01'),
('AGR000003', 'Amit', 'Singh', 'Verma', 1, 2, 1, 1, 'amit.verma@company.com', '9876543212', '2023-01-20'),

-- Sales Department Employees
('SAL000001', 'Sunita', NULL, 'Gupta', 2, 3, 1, 1, 'sunita.gupta@company.com', '9876543213', '2023-03-01'),
('SAL000002', 'Vikash', 'Kumar', 'Singh', 2, 3, 1, 1, 'vikash.singh@company.com', '9876543214', '2023-02-15'),
('SAL000003', 'Meera', NULL, 'Joshi', 2, 4, 1, 1, 'meera.joshi@company.com', '9876543215', '2023-01-10'),

-- Marketing Department Employees
('MKT000001', 'Arjun', 'Kumar', 'Reddy', 3, 5, 1, 1, 'arjun.reddy@company.com', '9876543216', '2023-04-01'),
('MKT000002', 'Kavita', NULL, 'Sharma', 3, 6, 1, 1, 'kavita.sharma@company.com', '9876543217', '2023-03-15'),

-- Finance Department Employees
('FIN000001', 'Rohit', 'Kumar', 'Agarwal', 4, NULL, 1, 1, 'rohit.agarwal@company.com', '9876543218', '2023-02-20'),
('FIN000002', 'Neha', NULL, 'Bansal', 4, NULL, 1, 1, 'neha.bansal@company.com', '9876543219', '2023-01-25'),

-- HR Department Employees
('HR000001', 'Deepak', 'Singh', 'Chauhan', 5, NULL, 1, 1, 'deepak.chauhan@company.com', '9876543220', '2023-01-05'),

-- IT Department Employees
('IT000001', 'Sanjay', 'Kumar', 'Mishra', 6, NULL, 1, 1, 'sanjay.mishra@company.com', '9876543221', '2023-03-10');

-- =====================================================
-- 3. INSERT EMPLOYEE ROLE ASSIGNMENTS
-- =====================================================

INSERT INTO EmployeeRoleAssignments (EmployeeID, RoleID, AssignedDate) VALUES
(1, 2, '2023-01-15'), -- Rajesh as Executive
(2, 3, '2023-02-01'), -- Priya as Associate
(3, 3, '2023-01-20'), -- Amit as Associate
(4, 1, '2023-03-01'), -- Sunita as Manager
(5, 2, '2023-02-15'), -- Vikash as Executive
(6, 3, '2023-01-10'), -- Meera as Associate
(7, 1, '2023-04-01'), -- Arjun as Manager
(8, 2, '2023-03-15'), -- Kavita as Executive
(9, 4, '2023-02-20'), -- Rohit as Analyst
(10, 4, '2023-01-25'), -- Neha as Analyst
(11, 1, '2023-01-05'), -- Deepak as Manager
(12, 2, '2023-03-10'); -- Sanjay as Executive

-- =====================================================
-- 4. INSERT SAMPLE TARGETS
-- =====================================================

INSERT INTO EmployeeTargets (EmployeeID, CategoryID, TargetValue, TargetPeriod, StartDate, EndDate) VALUES
-- Sales targets for sales team
(4, 1, 500000.00, 'Monthly', '2024-01-01', '2024-01-31'),
(5, 1, 400000.00, 'Monthly', '2024-01-01', '2024-01-31'),
(6, 1, 300000.00, 'Monthly', '2024-01-01', '2024-01-31'),

-- Revenue targets for managers
(4, 2, 1500000.00, 'Quarterly', '2024-01-01', '2024-03-31'),
(7, 2, 1200000.00, 'Quarterly', '2024-01-01', '2024-03-31'),
(11, 2, 800000.00, 'Quarterly', '2024-01-01', '2024-03-31'),

-- Customer acquisition targets
(4, 3, 50.00, 'Monthly', '2024-01-01', '2024-01-31'),
(5, 3, 40.00, 'Monthly', '2024-01-01', '2024-01-31'),
(6, 3, 30.00, 'Monthly', '2024-01-01', '2024-01-31');
