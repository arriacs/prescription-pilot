# Importing and Creating a Database for Drugs@FDA Data in MySQL
from pathlib import Path

content = r"""# Drugs@FDA MySQL Workbench Setup Guide

This guide explains how to set up the Drugs@FDA data in MySQL Workbench using the graphical interface, including which menus and buttons to click. It also documents fixes for import problems encountered during setup.

> **Important:** The FDA text files and your MySQL table definitions must match. The import steps below explain how to use Workbench, but do not assume every file has the same character encoding or column order. Check each file's header and the corresponding table definition before importing.

## 1. What you need first

Install or open:

- **MySQL Server** — the database service.
- **MySQL Workbench** — the graphical program used to connect to MySQL and run SQL.
- The Drugs@FDA tab-delimited text files downloaded from the FDA's official [Drugs@FDA Data Files page](https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files).

Download the files to a folder on your computer. Keep the files as downloaded; do not open and resave them in Excel, because that can change their formatting or values.

## 2. Open MySQL Workbench and connect to the server

1. Open **MySQL Workbench**.
2. On the home screen, find **MySQL Connections**.
3. Double-click the connection you use for your local MySQL Server.
4. If prompted, enter your MySQL password and click **OK**.
5. Wait for the SQL Editor window to open.

If you do not already have a connection:
1. On the Workbench home screen, click the **+** next to **MySQL Connections**.
2. In **Setup New Connection**, enter a name such as `Local MySQL`.
3. Leave **Connection Method** as `Standard (TCP/IP)` unless your class or installation specifies otherwise.
4. For a typical local installation, use hostname `127.0.0.1`, port `3306`, and your MySQL username.
5. Click **Test Connection**.
6. If the test succeeds, click **OK**, then double-click the new connection.

The exact hostname, username, and password depend on your MySQL installation. Do not put your password in this README or commit it to Git.

## 3. Enable local file imports

MySQL Workbench may block `LOAD DATA LOCAL INFILE` until it is enabled on both the server and the Workbench connection.

### 3A. Enable it on the MySQL server

1. Connect to your server as described above.
2. In the SQL Editor, click the **New SQL Tab** button (the page icon with a plus), or use **File → New Query Tab**.
3. Copy and paste the following into the query tab:

   ```sql
   SET GLOBAL local_infile = 1;
   SHOW GLOBAL VARIABLES LIKE 'local_infile';
   ```

4. Click the **lightning bolt** button to execute the selected query or the whole query tab. If Workbench asks which statements to run, run both.
5. In the **Result Grid**, check that `local_infile` is `ON`.

If the `SET GLOBAL` statement reports an access/permission error, reconnect with a MySQL account that has permission to change global variables, or ask the database administrator/instructor to enable it.

### 3B. Enable it for the Workbench connection

1. Return to the Workbench **Home** screen. If necessary, click the **Home** icon in the upper-left.
2. Under **MySQL Connections**, right-click your connection and choose **Edit Connection**. Depending on the Workbench version, you can also click the wrench icon shown when hovering over the connection.
3. Open the **Advanced** tab.
4. Find the **Others** text box.
5. Add this setting on its own line:

   ```text
   OPT_LOCAL_INFILE=1
   ```

   If the box already contains other settings, keep them and add a space or a new line before this setting.

6. Click **Test Connection** if available, then click **OK** to save.
7. Close the existing SQL Editor connection and reconnect by double-clicking the connection again. The connection must be reopened for the client setting to take effect.

If you still get Error 3948 or 3950, check both 3A and 3B, then disconnect and reconnect once more.

## 4. Create the database (schema)

1. Connect to MySQL Workbench.
2. Open a new SQL tab.
3. Paste and execute:

   ```sql
   CREATE DATABASE IF NOT EXISTS drugs_fda;
   USE drugs_fda;
   ```

4. Click the **lightning bolt** to execute.
5. On the left, locate the **SCHEMAS** panel.
6. Click the small **refresh** icon next to `SCHEMAS` if `drugs_fda` does not appear.
7. Expand `drugs_fda` using the triangle next to its name.

You should use the `drugs_fda` schema for the tables and imports in this project.

## 5. Create the tables

The project uses these table names:

- `ActionTypes_Lookup`
- `ApplicationDocs`
- `Applications`
- `ApplicationsDocsType_Lookup`
- `Join_Submission_ActionType_Lookup`
- `MarketingStatus`
- `MarketingStatus_Lookup`
- `Products`
- `SubmissionClass_Lookup`
- `SubmissionPropertyType`
- `Submissions`
- `TE`

### Option A: Run your table-creation SQL file

Use this if your project already has a `.sql` file containing `CREATE TABLE` statements.

1. In Workbench, choose **File → Open SQL Script**.
2. Browse to your project's table-creation script and select it.
3. Click **Open**. The script appears in a SQL tab.
4. At the top of the SQL Editor, set the default schema to `drugs_fda` using the schema dropdown, if one is shown. Otherwise, make sure the script includes `USE drugs_fda;` before its `CREATE TABLE` statements.
5. Click the **lightning bolt** to run the script.
6. Read the **Action Output** panel at the bottom. Check for red error icons or messages.
7. In the left **SCHEMAS** panel, expand `drugs_fda` → **Tables**. Right-click **Tables** and choose **Refresh All** if the new tables do not appear.

### Option B: Create tables manually in Workbench

Use this only if you do not have a table-creation script.

1. In the **SCHEMAS** panel, expand `drugs_fda`.
2. Right-click **Tables** and choose **Create Table**.
3. Enter the table name.
4. Add every column with the correct name and data type.
5. Select the **PK** checkbox for the primary-key column. Select **NN** if the column must not be `NULL`; use **AI** only if the ID is generated by MySQL and is not present in the source file.
6. Add foreign keys using the **Foreign Keys** tab when the table relationships are known.
7. Click **Apply**.
8. Review the generated SQL in the confirmation window and click **Apply** again, then **Finish**.
9. Repeat for each table.

**Do not guess the columns or data types.** Open each downloaded text file in a plain-text editor and inspect its first line/header, then compare it with the `CREATE TABLE` definition. The number, order, and meaning of source fields must line up with the import mapping. If a source file does not have a generated ID column, do not blindly import a source field into that ID column.

## 6. Check a downloaded file before importing it

For each file you plan to import:

1. Open **File Explorer** and navigate to the folder where you saved the FDA files.
2. Right-click the `.txt` file and choose **Open with → Notepad** (or another plain-text editor).
3. Inspect the first line. Confirm whether it contains column names and note the exact order.
4. Check that the file appears tab-delimited. Do not use commas as the delimiter if the file is tab-delimited.
5. Close the file without saving changes.
6. In Workbench, compare the source columns with the target table's columns. You can inspect the table definition with:

   ```sql
   USE drugs_fda;
   DESCRIBE Applications;
   ```

   Replace `Applications` with the table you are checking. Execute using the lightning bolt; the result grid shows the column names and data types.

If the text file has no header row, do not use `IGNORE 1 LINES` in the import statement. If it has a header row, use `IGNORE 1 LINES`.

## 7. Import a tab-delimited text file using SQL

This method is useful when the Workbench **Table Data Import Wizard** does not give enough control over data types, column order, blank values, or character encoding.

### 7A. Open a query tab

1. In Workbench, click **File → New Query Tab** (or click the **New SQL Tab** icon).
2. Enter `USE drugs_fda;` at the top.
3. Add a `LOAD DATA LOCAL INFILE` statement. Replace the example file path and table name with your actual values.

   ```sql
   USE drugs_fda;

   LOAD DATA LOCAL INFILE 'C:/path/to/your/data/Applications.txt'
   INTO TABLE Applications
   FIELDS TERMINATED BY '\\t'
   OPTIONALLY ENCLOSED BY '"'
   LINES TERMINATED BY '\\r\\n'
   IGNORE 1 LINES;
   ```

4. Use forward slashes `/` in Windows paths, or escape backslashes as `\\\\`.
5. Check the filename, table name, line ending, header, and column mapping before running.
6. Click the **lightning bolt** to execute the statement.
7. Look at the **Action Output** panel. It reports how many rows were loaded, skipped, or generated warnings.
8. If warnings appear, click or inspect the warning details and resolve them before using the data for analysis.

The example assumes a Windows text file with CRLF line endings and a header row. If the file uses LF line endings, use `LINES TERMINATED BY '\\n'`. Use the actual file format rather than copying the example blindly.

### 7B. Alternative: use the Table Data Import Wizard

The wizard is useful for straightforward files, but it may not provide the control needed for the problems documented below.

1. In the **SCHEMAS** panel, expand `drugs_fda` → **Tables**.
2. Right-click the target table and choose **Table Data Import Wizard**.
3. Click **Browse** and select the appropriate `.txt` or `.csv` file.
4. Click **Next**.
5. Confirm the destination schema and table. If the wizard offers delimiter or format options, choose the tab delimiter for FDA tab-delimited files.
6. Review the column mapping carefully. Do not map a text code to an integer ID column just because the columns appear next to each other.
7. Click **Next**, then **Import** or **Finish**, depending on your Workbench version.
8. Review the import summary and any warnings.

If the wizard maps columns incorrectly or cannot handle blank values/encoding, cancel and use the SQL method in 7A with an explicit column mapping.

## 8. Fixes for import errors encountered in this project

### Problem A: `LOAD DATA LOCAL INFILE` is disabled (Error 3948 or 3950)

**What to do:**
1. Follow Section 3A to enable `local_infile` on the server.
2. Follow Section 3B to add `OPT_LOCAL_INFILE=1` to the Workbench connection.
3. Disconnect and reconnect to the connection.
4. Try the import again.

Both the server and client must permit local file loading.

### Problem B: `Invalid utf8mb4 character string` during the `Submissions` import

A `Submissions` import failed around text including `Label for Men` with an invalid-character-set error. Changing the import to use `CHARACTER SET latin1` allowed that particular import to proceed.

For example, the placement in the statement is:

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/data/Submissions.txt'
INTO TABLE Submissions
CHARACTER SET latin1
FIELDS TERMINATED BY '\\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES;
```

**Caution:** This was a workaround for that file/error, not proof that every FDA file uses `latin1`. Inspect the file's encoding when possible. After importing, check for warnings and confirm text values look correct.

### Problem C: blank `SubmissionClassCodeID` values cause integer warnings

The `Submissions` import loaded **194,130 rows with 11,896 warnings**. The warnings included blank values being interpreted as integers.

If a blank source field means “missing” in your dataset and the table column allows `NULL`, load the field into a user variable and convert empty strings to `NULL`. The following is a pattern; the complete field list must match the actual file header and table definition:

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/data/Submissions.txt'
INTO TABLE Submissions
FIELDS TERMINATED BY '\\t'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
(
  @field1,
  @field2,
  @SubmissionClassCodeID,
  @field4
)
SET SubmissionClassCodeID = NULLIF(@SubmissionClassCodeID, '');
```

Replace the example variables with **every field in the actual file, in exact source order**. Do not paste this abbreviated mapping unchanged into a real import. Use this only if blank values should truly become `NULL` and the column permits it. Do not re-import into a populated table without deciding how duplicates will be handled.

### Problem D: duplicate primary-key warnings or “0 rows affected”

Some imports reported that rows were skipped because of duplicate keys. Tables affected included `ActionTypes_Lookup`, `ApplicationDocs`, `Products`, `MarketingStatus_Lookup`, `SubmissionClass_Lookup`, and `SubmissionPropertyType`.

This often means the table already contains the rows, perhaps because the import was run previously. It does **not** by itself prove the table is complete or correct.

1. Run a count query (Section 9).
2. Check a few rows with `SELECT * FROM table_name LIMIT 10;`.
3. Check the **Action Output** warning details.
4. Do not repeatedly import the same file without checking the table first.
5. Do not use `TRUNCATE TABLE` unless you intentionally want to remove all rows and understand the foreign-key relationships. Truncating is destructive.

### Problem E: a text code is being inserted into an integer column

The import into `Join_Submission_ActionType_Lookup` showed a warning in which the value `SUPPL` was assigned to the integer column `J_SubmissionActionTypeID`. That is a sign the source-to-table column mapping is likely wrong.

**Do not use this table for analysis until you check it.**

1. Open the source `Join_Submission_ActionTypes_Lookup.txt` file in Notepad and inspect the header and first few data lines.
2. In Workbench, run:

   ```sql
   DESCRIBE Join_Submission_ActionType_Lookup;
   SELECT * FROM Join_Submission_ActionType_Lookup LIMIT 10;
   ```

3. Compare each source field with the target column in order.
4. Correct the table definition or, preferably, the `LOAD DATA` field list so that each source value is assigned to the correct column.
5. If the table already contains incorrectly imported rows, do not just run the corrected import on top of them. Decide whether to clear and reload the table, accounting for foreign keys and any data you need to preserve.

### Problem F: `ProductNo` is truncated or values appear in the wrong columns

Warnings during imports of `Products` and `MarketingStatus` included `ProductNo` truncation. This can indicate that the column is too short, the source fields are mapped in the wrong order, or the file format has been interpreted incorrectly.

1. Run `DESCRIBE Products;` or `DESCRIBE MarketingStatus;`.
2. Inspect the source file's header and first few lines in Notepad.
3. Check the declared size/type of `ProductNo` and compare it with the actual source values.
4. Verify the import field order before retrying.
5. Fix the table definition or import mapping, then reload safely if necessary.

### Problem G: import succeeds but warning count is not zero

An import can report a large row count and still contain data-quality problems. For example, the `Submissions` import completed with 11,896 warnings. Do not ignore warnings automatically.

1. Read the warning text in **Action Output**.
2. Identify whether the warning is caused by duplicates, invalid characters, truncated values, or blank-to-number conversion.
3. Fix the cause.
4. Verify row counts and sample values before analysis.

## 9. Verify that tables contain data

Open a new query tab and execute:

```sql
USE drugs_fda;

SELECT 'Applications' AS table_name, COUNT(*) AS row_count FROM Applications
UNION ALL
SELECT 'Submissions', COUNT(*) FROM Submissions
UNION ALL
SELECT 'Products', COUNT(*) FROM Products
UNION ALL
SELECT 'TE', COUNT(*) FROM TE
UNION ALL
SELECT 'MarketingStatus', COUNT(*) FROM MarketingStatus
UNION ALL
SELECT 'ApplicationDocs', COUNT(*) FROM ApplicationDocs;
```

To inspect a table, run a query such as:

```sql
SELECT * FROM Applications LIMIT 10;
SELECT * FROM Submissions LIMIT 10;
```

To check missing submission class codes:

```sql
SELECT COUNT(*) AS missing_submission_class_code
FROM Submissions
WHERE SubmissionClassCodeID IS NULL;
```

Use the **Result Grid** to inspect the returned values. A row count alone does not prove that fields were mapped correctly; look at actual sample rows too.

## 10. Save your SQL scripts in the GitHub project

Keep repeatable setup and import steps in `.sql` files rather than only in a Workbench query tab.

Suggested project layout:

```text
Prescription_Pilot/
├── README.md
└── sql/
    ├── create_tables.sql
    ├── import_data.sql
    └── eda.sql
```

To save a query tab as a script:

1. In the SQL Editor, click **File → Save Script As...** (or **Save SQL Script As...**, depending on version).
2. Browse to your local `Prescription_Pilot` project folder.
3. Create a folder named `sql` if it does not exist.
4. Save table creation statements as `create_tables.sql`, import statements as `import_data.sql`, and analysis queries as `eda.sql`.
5. Review each script to ensure it does not contain your password or machine-specific paths that other team members cannot use.

## 11. Commit the README and SQL scripts to GitHub

If you use VS Code:

1. Open VS Code and choose **File → Open Folder...**.
2. Select the local `Prescription_Pilot` repository folder.
3. In the left sidebar, click **Source Control** (the branching icon).
4. Review the changed files.
5. Click the **+** next to each file you want to stage, or click **Stage All Changes**.
6. Enter a commit message such as `Document Drugs@FDA database setup`.
7. Click **Commit**.
8. Click **Sync Changes** or **Push** to send the commit to GitHub. If asked to sign in or authorize GitHub, follow the prompts.

Alternatively, use a terminal opened in the repository folder:

```bash
git status
git add README.md sql/
git commit -m "Document Drugs@FDA database setup"
git push
```

Only stage paths that exist and that you intend to commit. Do not commit raw FDA data files, database passwords, or other credentials unless your project explicitly requires them and you have confirmed it is appropriate.

## 12. Quick checklist

- [ ] MySQL Server is running and Workbench can connect.
- [ ] `local_infile` is `ON` on the server.
- [ ] `OPT_LOCAL_INFILE=1` is saved in the Workbench connection settings.
- [ ] `drugs_fda` schema exists.
- [ ] All required tables exist.
- [ ] Every source file's header and column order were checked before importing.
- [ ] Imports were run into the intended tables.
- [ ] Import warnings were reviewed and resolved or documented.
- [ ] Row counts and sample rows were checked.
- [ ] `Join_Submission_ActionType_Lookup` was checked for incorrect field mapping.
- [ ] SQL scripts and README are saved in the project repository.
- [ ] No passwords or unintended raw data files are committed.

## Official reference

- FDA, Drugs@FDA Data Files: https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files
- MySQL Reference Manual, `LOAD DATA`: https://dev.mysql.com/doc/refman/8.4/en/load-data.html
- MySQL Reference Manual, `LOAD DATA LOCAL` security considerations: https://dev.mysql.com/doc/refman/8.4/en/load-data-local-security.html
"""
path = Path("/mnt/data/README.md")
path.write_text(content, encoding="utf-8")
print(f"Created {path} ({len(content.splitlines())} lines, {path.stat().st_size} bytes)")

