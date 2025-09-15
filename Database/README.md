# Employee Management Database Schema

This database schema provides a comprehensive hierarchical structure for managing employee data with proper primary key identity management and departmental organization.

## 📋 Schema Overview

The database is designed with the following key principles:
- **Hierarchical Department Structure** - Supports multi-level department organization
- **Identity Primary Keys** - All tables use `IDENTITY(1,1)` for auto-incrementing primary keys
- **Referential Integrity** - Proper foreign key relationships maintain data consistency
- **Audit Trail** - Created/Modified timestamps and user tracking
- **Performance Optimized** - Strategic indexes for fast queries

## 🏗️ Database Structure

### Core Tables

#### 1. Department Hierarchy
```sql
Departments
├── DepartmentID (PK, Identity)
├── DepartmentCode (Unique)
├── DepartmentName
├── ParentDepartmentID (Self-referencing FK)
└── Audit fields

SubDepartments
├── SubDepartmentID (PK, Identity)
├── DepartmentID (FK to Departments)
├── SubDepartmentCode
└── SubDepartmentName
```

#### 2. Employee Core Tables
```sql
Employees (Main Table)
├── EmployeeID (PK, Identity)
├── EmployeeCode (Unique)
├── Personal Information (Names, Contact)
├── DepartmentID (FK)
├── SubDepartmentID (FK)
├── EmployeeTypeID (FK)
├── StatusID (FK)
└── Audit fields

EmployeeStatus
├── StatusID (PK, Identity)
├── StatusCode (ACTIVE, INACTIVE, TERMINATED)
└── StatusName

EmployeeTypes
├── TypeID (PK, Identity)
├── TypeCode (FTE, PTE, CONTRACT, INTERN)
└── TypeName
```

#### 3. Target Management
```sql
EmployeeTargets
├── TargetID (PK, Identity)
├── EmployeeID (FK)
├── CategoryID (FK)
├── TargetValue
├── TargetPeriod (Monthly, Quarterly, Yearly)
└── Date ranges

TargetCategories
├── CategoryID (PK, Identity)
├── CategoryCode
└── CategoryName
```

#### 4. Role Management
```sql
EmployeeRoles
├── RoleID (PK, Identity)
├── RoleCode
├── RoleName
└── DepartmentID (FK, Optional)

EmployeeRoleAssignments
├── AssignmentID (PK, Identity)
├── EmployeeID (FK)
├── RoleID (FK)
├── AssignedDate
└── UnassignedDate
```

## 🔍 Key Features

### 1. Identity Primary Keys
All tables use `INT IDENTITY(1,1)` primary keys for:
- **Auto-incrementing values** - No manual ID management required
- **Performance** - Integer keys provide optimal join performance
- **Consistency** - Standardized approach across all tables

### 2. Department Hierarchy
- **Multi-level structure** - Departments can have parent departments
- **Flexible organization** - Easy to reorganize department structure
- **Sub-departments** - Additional granular level within departments

### 3. Comprehensive Views
- `vw_EmployeeDetails` - Complete employee information with joins
- `vw_DepartmentHierarchy` - Hierarchical department structure with levels
- `vw_EmployeeTargetsSummary` - Target information with status
- `vw_DepartmentSummary` - Department statistics and metrics

### 4. Stored Procedures
- `sp_GetEmployeesByDepartment` - Retrieve employees by department
- `sp_GetEmployeeTargets` - Target performance queries
- `sp_AddEmployee` - Add new employee with validation
- `sp_GetDepartmentStatistics` - Department analytics

## 🚀 Usage Examples

### 1. Basic Employee Query
```sql
-- Get all active employees with department information
SELECT * FROM vw_EmployeeDetails
ORDER BY DepartmentName, FullName;
```

### 2. Department Hierarchy
```sql
-- View complete department hierarchy
SELECT 
    REPLICATE('  ', Level) + DepartmentName as HierarchyDisplay,
    EmployeeCount,
    HierarchyPath
FROM vw_DepartmentHierarchy
ORDER BY HierarchyCode;
```

### 3. Employee Targets
```sql
-- Get active targets for sales department
EXEC sp_GetEmployeeTargets 
    @DepartmentCode = 'SALES',
    @TargetPeriod = 'Monthly';
```

### 4. Add New Employee
```sql
-- Add a new employee with role assignment
EXEC sp_AddEmployee
    @EmployeeCode = 'IT000002',
    @FirstName = 'John',
    @LastName = 'Doe',
    @DepartmentCode = 'IT',
    @EmployeeTypeCode = 'FTE',
    @Email = 'john.doe@company.com',
    @RoleCode = 'EXEC';
```

### 5. Department Statistics
```sql
-- Get statistics for all departments
EXEC sp_GetDepartmentStatistics;

-- Get statistics for specific department
EXEC sp_GetDepartmentStatistics @DepartmentCode = 'SALES';
```

## 📊 Sample Data Structure

The schema includes sample data for:
- **6 Departments**: Agriculture, Sales, Marketing, Finance, HR, IT
- **12 Sample Employees** across different departments
- **Role Assignments** for each employee
- **Target Data** for sales and management roles
- **Sub-departments** for larger departments

## 🔧 Installation Instructions

1. **Create Database Schema**
   ```sql
   -- Run EmployeeSchema.sql to create all tables, indexes, and triggers
   ```

2. **Insert Sample Data**
   ```sql
   -- Run SampleData.sql to populate with sample data
   ```

3. **Create Views and Procedures**
   ```sql
   -- Run ViewsAndProcedures.sql to create views and stored procedures
   ```

## 🎯 Key Benefits

### For Developers
- **Clean Architecture** - Well-structured, normalized design
- **Performance Optimized** - Strategic indexes and efficient queries
- **Extensible** - Easy to add new features and relationships

### For Business Users
- **Hierarchical Reporting** - Department-wise employee organization
- **Target Tracking** - Performance management capabilities
- **Audit Trail** - Complete change tracking
- **Flexible Roles** - Dynamic role assignment system

### For Database Administrators
- **Identity Management** - Automatic primary key generation
- **Referential Integrity** - Consistent data relationships
- **Scalable Design** - Supports growth and organizational changes

## 🔒 Security Features

- **Foreign Key Constraints** - Prevent orphaned records
- **Data Validation** - Stored procedures include input validation
- **Audit Triggers** - Automatic tracking of modifications
- **Soft Deletes** - IsActive flags instead of hard deletes

## 📈 Performance Considerations

- **Strategic Indexes** - Optimized for common query patterns
- **Computed Columns** - FullName calculated automatically
- **Efficient Joins** - Integer primary keys for optimal performance
- **View Optimization** - Pre-joined data for common queries

## 🔄 Maintenance

### Regular Tasks
- Monitor index fragmentation
- Update statistics regularly
- Review audit logs
- Backup database regularly

### Schema Evolution
- Use ALTER statements for schema changes
- Maintain backward compatibility
- Update views and procedures as needed
- Test changes in development environment first

---

*This schema provides a solid foundation for employee management systems with proper hierarchy, identity management, and performance optimization.*
