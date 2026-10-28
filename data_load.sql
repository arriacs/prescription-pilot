USE drugs_fda;

-- 1. ActionTypes_Lookup
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/ActionTypes_Lookup.txt'
INTO TABLE ActionTypes_Lookup
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ActionTypes_LookupID, ActionTypes_LookupDescription,
 SupplCategoryLevel1Code, SupplCategoryLevel2Code);

-- 2. ApplicationDocs
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/ApplicationDocs.txt'
INTO TABLE ApplicationDocs
CHARACTER SET latin1
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplicationDocsID, ApplicationDocsTypeID, ApplNo,
 SubmissionType, SubmissionNo, ApplicationDocsTitle,
 ApplicationDocsURL, ApplicationDocsDate);

-- 3. Applications
-- Already imported; run only if you empty the table first.
-- LOAD DATA LOCAL INFILE
-- 'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/Applications.txt'
-- INTO TABLE Applications
-- FIELDS TERMINATED BY '\t'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\r\n'
-- IGNORE 1 LINES
-- (ApplNo, ApplType, ApplPublicNotes, SponsorName);

-- 4. ApplicationsDocsType_Lookup
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/ApplicationsDocsType_Lookup.txt'
INTO TABLE ApplicationsDocsType_Lookup
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplicationDocsType_Lookup_ID,
 ApplicationDocsType_Lookup_Description);

-- 5. Join_Submission_ActionTypes_Lookup
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/Join_Submission_ActionTypes_Lookup.txt'
INTO TABLE Join_Submission_ActionType_Lookup
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(J_SubmissionActionTypeID, SubmissionNo, SubmissionType,
 ApplNo, ActionTypes_LookupID);

-- 6. MarketingStatus
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/MarketingStatus.txt'
INTO TABLE MarketingStatus
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplNo, ProductNo, MarketingStatusID);

-- 7. MarketingStatus_Lookup
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/MarketingStatus_Lookup.txt'
INTO TABLE MarketingStatus_Lookup
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(MarketingStatusID, MarketingStatusDescription);

-- 8. Products
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/Products.txt'
INTO TABLE Products
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplNo, ProductNo, Form, Strength, ReferenceDrug,
 DrugName, ActiveIngredient, ReferenceStandard);

-- 9. SubmissionClass_Lookup
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/SubmissionClass_Lookup.txt'
INTO TABLE SubmissionClass_Lookup
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(SubmissionClassCodeID, SubmissionClassCode,
 SubmissionClassCodeDescription);

-- 10. SubmissionPropertyType
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/SubmissionPropertyType.txt'
INTO TABLE SubmissionPropertyType
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplNo, SubmissionType, SubmissionNo,
 SubmissionPropertyTypeCode, SubmissionPropertyTypeID);

-- 11. Submissions
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/Submissions.txt'
INTO TABLE Submissions
CHARACTER SET latin1
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplNo, SubmissionClassCodeID, SubmissionType,
 SubmissionNo, SubmissionStatus, SubmissionStatusDate,
 SubmissionsPublicNotes, ReviewPriority);

-- 12. TE
LOAD DATA LOCAL INFILE
'C:/Users/acts5/OneDrive - San Diego State University (SDSU.EDU)/SDSU/Prescription_Pilot/Drugs@FDA/dafdata20261014/TE.txt'
INTO TABLE TE
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(ApplNo, ProductNo, MarketingStatusID, TECode);
