-- Simple Employee Data - Based on Excel Image
-- Inserting sample records that match the visible Excel structure

INSERT INTO Employees (
    EmployeeID, DepartmentVertical, Names, Target,
    L1Name, L1EmployeeCode, L2Name, L2EmployeeID, L3Name, L3EmployeeID,
    L4Name, L4EmployeeID, L5Name, L5EmployeeID, L6Name, L6EmployeeID,
    L7Name, L7EmployeeID, L8Name, L8EmployeeID, L9Name, L9EmployeeID,
    L10Name, L10EmployeeID, L11Name, L11EmployeeID, L12Name, L12EmployeeID,
    L13Name, L13EmployeeID, L14Name, L14EmployeeID, L15Name, L15EmployeeID,
    L16Name, L16EmployeeID, L17Name, L17EmployeeID
) VALUES 
-- Sample records based on the Excel structure visible in the image
('AGR000001', 'AGRICULTURE', 'ACTIVE', '4000000', 'KAMLAJYOTI', 'PGL000000', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000002', 'AGRICULTURE', 'ACTIVE', '5000000', 'DHANANJAY', 'AGR100001', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000003', 'AGRICULTURE', 'ACTIVE', '0', 'Shivam Narendra Ghatge', 'AGR100076', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000004', 'AGRICULTURE', 'ACTIVE', '1500000', 'HEMANT KUMAR', 'AGR100007', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000005', 'AGRICULTURE', 'ACTIVE', '1200000', 'SHAILESH KUMAR', 'AGR100001', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000006', 'AGRICULTURE', 'ACTIVE', '1000000', 'RAHUL TIWARI', 'AGR100007', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000007', 'AGRICULTURE', 'ACTIVE', '1200000', 'HEMANT KUMAR', 'AGR100001', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000008', 'AGRICULTURE', 'ACTIVE', '700000', 'SANDEEP KUMAR SHUKLA', 'AGR100043', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000009', 'AGRICULTURE', 'ACTIVE', '0', 'Shivam Narendra Ghatge', 'AGR100076', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'),

('AGR000010', 'AGRICULTURE', 'ACTIVE', '1200000', 'HEMANT KUMAR', 'AGR100001', 'Ajeet Singh Choudhary', 'PGL000099', 'Rupam Seth', '0001000000', 'GAURAV CHAUBEY', 'PGL000098', 'Santanu Agarwal', 'PGL000097', 'Surat Agarwal', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');
