CREATE DATABASE ShortLeaveDB;

USE ShortLeaveDB;
CREATE TABLE Employee
(
    EmployeeId INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeCode VARCHAR(20) UNIQUE,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255),
    Department VARCHAR(50),
    Designation VARCHAR(50),
    Mobile VARCHAR(15),
    Status BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Admin
(
    AdminId INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO Admin
(
FullName,
Email,
Password
)
VALUES
(
'Administrator',
'admin@gmail.com',
''
);
SELECT * FROM admin;
-- 1. Leave Balance
CREATE TABLE LeaveBalance
(
    BalanceId INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeId INT NOT NULL,
    CasualLeave DECIMAL(5,1) DEFAULT 12,
    SickLeave DECIMAL(5,1) DEFAULT 10,
    PaidLeave DECIMAL(5,1) DEFAULT 15,
    UsedCasualLeave DECIMAL(5,1) DEFAULT 0,
    UsedSickLeave DECIMAL(5,1) DEFAULT 0,
    UsedPaidLeave DECIMAL(5,1) DEFAULT 0,

    FOREIGN KEY (EmployeeId)
    REFERENCES Employee(EmployeeId)
    ON DELETE CASCADE
);
CREATE TABLE LeaveRequest
(
    LeaveId INT AUTO_INCREMENT PRIMARY KEY,

    EmployeeId INT NOT NULL,

    LeaveType VARCHAR(30) NOT NULL,

    FromDate DATE NOT NULL,
    ToDate DATE NOT NULL,

    TotalDays DECIMAL(5,1) NOT NULL,

    Reason VARCHAR(500),

    Status VARCHAR(20) DEFAULT 'Pending',

    AppliedDate DATE DEFAULT (CURRENT_DATE),

    AppliedTime TIME DEFAULT (CURRENT_TIME),

    ApprovedBy INT NULL,

    ApprovedDate DATETIME NULL,

    ManagerRemark VARCHAR(500),

    FOREIGN KEY (EmployeeId)
    REFERENCES Employee(EmployeeId)
    ON DELETE CASCADE
);
CREATE TABLE Holiday
(
    HolidayId INT AUTO_INCREMENT PRIMARY KEY,
    HolidayDate DATE NOT NULL UNIQUE,
    HolidayName VARCHAR(100) NOT NULL
);
CREATE TABLE Notification
(
    NotificationId INT AUTO_INCREMENT PRIMARY KEY,

    LeaveId INT NULL,

    EmployeeId INT NOT NULL,

    Title VARCHAR(200),

    Message VARCHAR(500),

    IsRead BOOLEAN DEFAULT FALSE,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (LeaveId)
    REFERENCES LeaveRequest(LeaveId)
    ON DELETE CASCADE,

    FOREIGN KEY (EmployeeId)
    REFERENCES Employee(EmployeeId)
    ON DELETE CASCADE
);
CREATE TABLE LeaveReasonSuggestion
(
    SuggestionId INT AUTO_INCREMENT PRIMARY KEY,

    LeaveType VARCHAR(30),

    SuggestionText VARCHAR(500),

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO LeaveReasonSuggestion
(LeaveType, SuggestionText)
VALUES
('Sick Leave', 'I am not feeling well and need rest.'),
('Casual Leave', 'I have some personal work to attend to.'),
('Paid Leave', 'I would like to take leave for personal reasons.'),
('Emergency Leave', 'Due to an unexpected emergency, I am unable to attend work.');

SHOW TABLES;
SELECT * FROM LeaveReasonSuggestion;
CREATE TABLE CompanySetting
(
    SettingId INT AUTO_INCREMENT PRIMARY KEY,

    WorkingDaysPerWeek INT NOT NULL DEFAULT 5,

    MondayWorking BOOLEAN DEFAULT TRUE,
    TuesdayWorking BOOLEAN DEFAULT TRUE,
    WednesdayWorking BOOLEAN DEFAULT TRUE,
    ThursdayWorking BOOLEAN DEFAULT TRUE,
    FridayWorking BOOLEAN DEFAULT TRUE,
    SaturdayWorking BOOLEAN DEFAULT FALSE,
    SundayWorking BOOLEAN DEFAULT FALSE,

    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
INSERT INTO CompanySetting
(
    WorkingDaysPerWeek,
    MondayWorking,
    TuesdayWorking,
    WednesdayWorking,
    ThursdayWorking,
    FridayWorking,
    SaturdayWorking,
    SundayWorking
)
VALUES
(
    5,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    FALSE,
    FALSE
);
SELECT * FROM CompanySetting;
SELECT * FROM Holiday;
SHOW TABLES;
SELECT * FROM leaverequest;
USE shortleavedb;

CREATE TABLE Attendance
(
    AttendanceId INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeId INT NOT NULL,
    AttendanceDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Present',
    InTime TIME NULL,
    OutTime TIME NULL,
    WorkingHours DECIMAL(5,2) NOT NULL DEFAULT 0,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE Holiday
ADD COLUMN HolidayType VARCHAR(30) NOT NULL DEFAULT 'Holiday',
ADD COLUMN Description VARCHAR(500) NULL,
ADD COLUMN CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
DESCRIBE Holiday;
CREATE TABLE LeaveStatusHistory
(
    HistoryId INT AUTO_INCREMENT PRIMARY KEY,
    LeaveId INT NOT NULL,
    OldStatus VARCHAR(50) NOT NULL,
    NewStatus VARCHAR(50) NOT NULL,
    ChangedBy INT NULL,
    Remark VARCHAR(500),
    ChangedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (LeaveId)
        REFERENCES LeaveRequest(LeaveId)
);
SELECT EmployeeId, FullName, Email, Status
FROM Employee;
UPDATE LeaveBalances
SET
    CasualLeave = 12,
    SickLeave = 12,
    PaidLeave = 15,
    UsedCasualLeave = 0,
    UsedSickLeave = 0,
    UsedPaidLeave = 0
WHERE EmployeeId = 1;
USE shortleavedb;

CREATE TABLE LeaveBalances
(
    LeaveBalanceId INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeId INT NOT NULL,

    CasualLeave DECIMAL(5,2) NOT NULL DEFAULT 12,
    SickLeave DECIMAL(5,2) NOT NULL DEFAULT 12,
    PaidLeave DECIMAL(5,2) NOT NULL DEFAULT 15,

    UsedCasualLeave DECIMAL(5,2) NOT NULL DEFAULT 0,
    UsedSickLeave DECIMAL(5,2) NOT NULL DEFAULT 0,
    UsedPaidLeave DECIMAL(5,2) NOT NULL DEFAULT 0,

    UNIQUE(EmployeeId)
);
SHOW TABLES;

SELECT * FROM LeaveBalance;
INSERT INTO LeaveBalance
(
    EmployeeId,
    CasualLeave,
    SickLeave,
    PaidLeave,
    UsedCasualLeave,
    UsedSickLeave,
    UsedPaidLeave
)
SELECT
    e.EmployeeId,
    12,
    10,
    15,
    0,
    0,
    0
FROM Employee e
LEFT JOIN LeaveBalance lb
    ON e.EmployeeId = lb.EmployeeId
WHERE lb.EmployeeId IS NULL;
USE ShortLeaveDB;

SELECT * FROM Employee;
USE ShortLeaveDB;

ALTER TABLE Employee
CHANGE COLUMN Name FullName VARCHAR(100) NOT NULL;

ALTER TABLE Employee
ADD COLUMN EmployeeCode VARCHAR(20) NULL,
ADD COLUMN Email VARCHAR(100) NULL,
ADD COLUMN Password VARCHAR(255) NULL,
ADD COLUMN Designation VARCHAR(50) NULL,
ADD COLUMN Mobile VARCHAR(15) NULL,
ADD COLUMN Status BOOLEAN NOT NULL DEFAULT TRUE,
ADD COLUMN CreatedAt DATETIME NULL;
SELECT * FROM Employee;
USE ShortLeaveDB;

CREATE TABLE LeaveStatusHistories (
    HistoryId INT AUTO_INCREMENT PRIMARY KEY,
    LeaveId INT NOT NULL,
    OldStatus VARCHAR(50) NOT NULL,
    NewStatus VARCHAR(50) NOT NULL,
    ChangedBy INT NULL,
    Remark VARCHAR(500) NOT NULL,
    ChangedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT FK_LeaveStatusHistories_LeaveRequest
        FOREIGN KEY (LeaveId)
        REFERENCES LeaveRequests(LeaveId)
        ON DELETE CASCADE
);
SHOW TABLES;
USE ShortLeaveDB;

DESCRIBE leavestatushistory;
UPDATE Employee
SET Email = 'amitpal3223@gmail.com'
WHERE EmployeeId = 1;
USE ShortLeaveDB;

ALTER TABLE Employee
ADD COLUMN ExitDate DATETIME NULL;
DESCRIBE Employee;
USE ShortLeaveDB;

ALTER TABLE Employee;

USE ShortLeaveDB;
ALTER TABLE LeaveRequest
ADD COLUMN ApprovedDays DECIMAL(10,2) NOT NULL DEFAULT 0;
ALTER TABLE LeaveRequests
ADD COLUMN ApprovedDays DECIMAL(10,2) NULL;
DESCRIBE LeaveRequest;
ALTER TABLE LeaveRequest
ADD COLUMN ApprovedDate DATETIME NULL,
ADD COLUMN ManagerRemark VARCHAR(500) NULL;
ALTER TABLE LeaveRequest

ADD COLUMN ManagerRemark VARCHAR(500) NULL;
USE ShortLeaveDB;

DESCRIBE LeaveRequest;
USE ShortLeaveDB;

RENAME TABLE LeaveRequest TO LeaveRequests;
SHOW TABLES;
USE ShortLeaveDB;

DESCRIBE leaverequests;
USE ShortLeaveDB;

ALTER TABLE leaverequests
ADD COLUMN ApprovedDays DECIMAL(10,2) NULL;
USE ShortLeaveDB;

SHOW TABLES;
ALTER TABLE LeaveRequests
ADD COLUMN RejectedDays DECIMAL(10,2) NULL;
UPDATE LeaveRequests
SET RejectedDays = 0
WHERE RejectedDays IS NULL;
SET SQL_SAFE_UPDATES = 0;

SET SQL_SAFE_UPDATES = 0;

USE ShortLeaveDB;

SET SQL_SAFE_UPDATES = 0;

UPDATE LeaveRequests
SET ApprovedDays = 0
WHERE ApprovedDays IS NULL;

SET SQL_SAFE_UPDATES = 0;
UPDATE LeaveRequests
SET RejectedDays = 0
WHERE RejectedDays IS NULL;
SET SQL_SAFE_UPDATES = 1;
SELECT LeaveId, ApprovedDays, RejectedDays
FROM LeaveRequests;SET SQL_SAFE_UPDATES = 0;

UPDATE LeaveRequests
SET ApprovedDays = 0,
    RejectedDays = 0
WHERE LeaveId > 0
  AND (ApprovedDays IS NULL OR RejectedDays IS NULL);

SET SQL_SAFE_UPDATES = 1;
SELECT LeaveId, ApprovedDays, RejectedDays
FROM LeaveRequests;
SELECT LeaveId, ApprovedDays, RejectedDays
FROM LeaveRequests;
ALTER TABLE Admin
ADD COLUMN ResetToken VARCHAR(255) NULL,
ADD COLUMN ResetTokenExpiry DATETIME NULL;
ALTER TABLE Employee
ADD COLUMN ResetToken VARCHAR(255) NULL,
ADD COLUMN ResetTokenExpiry DATETIME NULL;
ALTER TABLE Admin
ADD COLUMN ResetOTP VARCHAR(6) NULL,
ADD COLUMN ResetOTPExpiry DATETIME NULL;

ALTER TABLE Employee
ADD COLUMN ResetOTP VARCHAR(6) NULL,
ADD COLUMN ResetOTPExpiry DATETIME NULL;
USE ShortLeaveDB;

DESCRIBE Employee;
ALTER TABLE Admin
ADD COLUMN ResetOTP VARCHAR(10) NULL,
ADD COLUMN ResetOTPExpiry DATETIME NULL;
USE ShortLeaveDB;


USE ShortLeaveDB;

SELECT * FROM Employee;
SELECT * FROM Attendance;
SELECT * FROM LeaveStatusHistory;