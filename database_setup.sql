USE drugs_fda;

-- Create the Drugs@FDA tables

-- 1. Applications
CREATE TABLE IF NOT EXISTS Applications (
	ApplNo CHAR(6) PRIMARY KEY,
    ApplType CHAR(5) NOT NULL,
    ApplPublicNotes TEXT,
    SponsorName VARCHAR(500));
    
-- 2. ActionTypes_Lookup
CREATE TABLE IF NOT EXISTS ActionTypes_Lookup (
    ActionTypes_LookupID INT AUTO_INCREMENT PRIMARY KEY,
    ActionTypes_LookupDescription VARCHAR(100) NOT NULL,
    SupplCategoryLevel1Code VARCHAR(100) NULL,
    SupplCategoryLevel2Code VARCHAR(100) NULL
);

-- 3. ApplicationDocs
CREATE TABLE IF NOT EXISTS ApplicationDocs (
    ApplicationDocsID INT AUTO_INCREMENT PRIMARY KEY,
    ApplicationDocsTypeID INT NOT NULL,
    ApplNo CHAR(6) NOT NULL,
    SubmissionType CHAR(10) NOT NULL,
    SubmissionNo INT NOT NULL,
    ApplicationDocsTitle VARCHAR(100) NULL,
    ApplicationDocsURL VARCHAR(200) NULL,
    ApplicationDocsDate DATETIME NULL
);

-- 4. ApplicationsDocsType_Lookup
CREATE TABLE IF NOT EXISTS ApplicationsDocsType_Lookup (
    ApplicationDocsType_Lookup_ID INT AUTO_INCREMENT PRIMARY KEY,
    ApplicationDocsType_Lookup_Description VARCHAR(200) NOT NULL
);

-- 5. Join_Submission_ActionType_Lookup
CREATE TABLE IF NOT EXISTS Join_Submission_ActionType_Lookup (
    J_SubmissionActionTypeID INT AUTO_INCREMENT PRIMARY KEY,
    SubmissionNo INT NOT NULL,
    SubmissionType CHAR(10) NOT NULL,
    ApplNo CHAR(6) NOT NULL,
    ActionTypes_LookupID INT NOT NULL
);

-- 6. MarketingStatus
CREATE TABLE IF NOT EXISTS MarketingStatus (
    ApplNo CHAR(6) NOT NULL,
    ProductNo CHAR(3) NOT NULL,
    MarketingStatusID INT NOT NULL,
    PRIMARY KEY (ApplNo, ProductNo, MarketingStatusID)
);

-- 7. MarketingStatus_Lookup
CREATE TABLE IF NOT EXISTS MarketingStatus_Lookup (
    MarketingStatusID INT AUTO_INCREMENT PRIMARY KEY,
    MarketingStatusDescription VARCHAR(200) NOT NULL
);

-- 8. Products
CREATE TABLE IF NOT EXISTS Products (
    ApplNo CHAR(6) NOT NULL,
    ProductNo CHAR(6) NOT NULL,
    Form VARCHAR(255) NULL,
    Strength VARCHAR(240) NULL,
    ReferenceDrug INT NULL,
    DrugName VARCHAR(125) NULL,
    ActiveIngredient VARCHAR(255) NULL,
    ReferenceStandard INT NULL,
    PRIMARY KEY (ApplNo, ProductNo)
);

-- 9. SubmissionClass_Lookup
CREATE TABLE IF NOT EXISTS SubmissionClass_Lookup (
    SubmissionClassCodeID INT AUTO_INCREMENT PRIMARY KEY,
    SubmissionClassCode VARCHAR(50) NOT NULL,
    SubmissionClassCodeDescription VARCHAR(500) NULL
);

-- 10. SubmissionPropertyType
CREATE TABLE IF NOT EXISTS SubmissionPropertyType (
    ApplNo CHAR(6) NOT NULL,
    SubmissionType CHAR(10) NOT NULL,
    SubmissionNo INT NOT NULL,
    SubmissionPropertyTypeCode VARCHAR(50) NOT NULL,
    SubmissionPropertyTypeID INT NOT NULL,
    PRIMARY KEY (
        ApplNo,
        SubmissionType,
        SubmissionNo,
        SubmissionPropertyTypeID
    )
);

-- 11. Submissions
CREATE TABLE IF NOT EXISTS Submissions (
    ApplNo CHAR(6) NOT NULL,
    SubmissionClassCodeID INT NULL,
    SubmissionType CHAR(10) NOT NULL,
    SubmissionNo INT NOT NULL,
    SubmissionStatus CHAR(2) NULL,
    SubmissionStatusDate DATETIME NULL,
    SubmissionsPublicNotes TEXT NULL,
    ReviewPriority VARCHAR(20) NULL,
    PRIMARY KEY (ApplNo, SubmissionType, SubmissionNo)
);

-- 12. TE
CREATE TABLE IF NOT EXISTS TE (
    ApplNo CHAR(6) NOT NULL,
    ProductNo CHAR(3) NOT NULL,
    MarketingStatusID INT NOT NULL,
    TECode VARCHAR(100) NOT NULL,
    PRIMARY KEY (ApplNo, ProductNo, MarketingStatusID, TECode)
);