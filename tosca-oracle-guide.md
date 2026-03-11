# TOSCA Automation for Oracle Server Applications
### Beginner → Intermediate Guide with Jenkins & Zephyr Integration

---

```
+------------------------------------------------------------------+
|           TOSCA ORACLE AUTOMATION LEARNING PATH                 |
+------------------------------------------------------------------+
|                                                                  |
|  [1. Test Automation Basics]  -->  [2. TOSCA Fundamentals]      |
|          |                                  |                    |
|          v                                  v                    |
|  [3. Oracle App Setup]    -->  [4. Intermediate Techniques]     |
|          |                                  |                    |
|          v                                  v                    |
|  [5. Jenkins Integration]  -->  [6. Zephyr Integration]         |
|                                                                  |
+------------------------------------------------------------------+
```

---

## Table of Contents

1. [Test Automation Basics](#1-test-automation-basics)
2. [TOSCA Fundamentals](#2-tosca-fundamentals)
3. [TOSCA Architecture](#3-tosca-architecture)
4. [Setting Up TOSCA for Oracle Applications](#4-setting-up-tosca-for-oracle-applications)
5. [Beginner: Your First TOSCA Test](#5-beginner-your-first-tosca-test)
6. [Intermediate: Advanced TOSCA Techniques](#6-intermediate-advanced-tosca-techniques)
7. [Jenkins Basics & TOSCA Integration](#7-jenkins-basics--tosca-integration)
8. [Zephyr Basics & Test Management](#8-zephyr-basics--test-management)
9. [End-to-End Workflow](#9-end-to-end-workflow)
10. [Cheat Sheet & Quick Reference](#10-cheat-sheet--quick-reference)

---

## 1. Test Automation Basics

### What Is Test Automation?

Test automation replaces manual, repetitive testing with scripts/tools that execute test cases automatically — validating application behavior without human interaction each time.

```
MANUAL TESTING                    AUTOMATED TESTING
+------------------+              +------------------+
|  Tester          |              |  Script/Tool     |
|  reads test case |              |  reads test case |
|  opens app       |    vs.       |  launches app    |
|  clicks buttons  |              |  executes steps  |
|  verifies result |              |  asserts result  |
|  writes result   |              |  logs result     |
|  (30 min each)   |              |  (30 sec each)   |
+------------------+              +------------------+
```

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \          <- Few, slow, high value
                 /  Tests \           (Selenium, TOSCA, Cypress)
                /----------\
               /            \
              / Integration  \     <- Moderate, API/DB level
             /    Tests       \       (Postman, REST Assured)
            /------------------\
           /                    \
          /     Unit Tests       \  <- Many, fast, low-level
         /   (most of your tests) \   (JUnit, PyTest, NUnit)
        /____________________________\
```

### Key Concepts

| Term | Definition |
|------|-----------|
| **Test Case** | A specific scenario with steps + expected outcomes |
| **Test Suite** | A collection of related test cases |
| **Test Plan** | Strategic document — what, when, who tests |
| **Test Execution** | Running tests and capturing results |
| **Test Coverage** | % of requirements validated by tests |
| **Regression Testing** | Re-running tests after changes to catch breakage |
| **Smoke Testing** | Quick sanity check — does the app start/work at all? |
| **Sanity Testing** | Focused check on a specific bug fix or feature |

### The Testing Lifecycle

```
+----------+    +----------+    +----------+    +----------+
| PLAN     | -> | DESIGN   | -> | EXECUTE  | -> | REPORT   |
|          |    |          |    |          |    |          |
| Define   |    | Write    |    | Run      |    | Analyze  |
| scope    |    | test     |    | tests    |    | results  |
| goals    |    | cases    |    | log bugs |    | metrics  |
| risks    |    | test data|    | retest   |    | coverage |
+----------+    +----------+    +----------+    +----------+
                                     ^
                                     |
                              [AUTOMATE THIS!]
```

### Why TOSCA for Oracle?

- **Model-based** — tests aren't fragile scripts, they're reusable models
- **No-code/low-code** — testers without deep coding skills can contribute
- **Oracle-aware** — built-in support for Oracle Forms, EBS, Fusion, ADF
- **Risk-based testing** — prioritizes high-impact areas automatically
- **CI/CD ready** — hooks directly into Jenkins pipelines

---

## 2. TOSCA Fundamentals

### What Is TOSCA?

**TOSCA** (Tricentis Optimization of Software Correctability Analysis) is a **model-based test automation** platform by Tricentis. Unlike script-based tools (Selenium, UFT), TOSCA uses a visual, model-driven approach.

```
SCRIPT-BASED (Selenium)             MODEL-BASED (TOSCA)
+---------------------------+       +---------------------------+
| driver.findElement(       |       |  [Module: Login Form]     |
|   By.id("username"))      |       |  - Username Field         |
|   .sendKeys("admin");     |  vs.  |  - Password Field         |
| driver.findElement(       |       |  - Login Button           |
|   By.id("password"))      |       |                           |
|   .sendKeys("pass");      |       |  [TestCase: Login_Admin]  |
| driver.findElement(       |       |  - Use: Login Form        |
|   By.id("loginBtn"))      |       |  - Enter credentials      |
|   .click();               |       |  - Verify dashboard       |
+---------------------------+       +---------------------------+
  Breaks on UI change                 Model updates once, all
                                      tests inherit the change
```

### Core TOSCA Components

```
+---------------------------------------------------------------+
|                    TOSCA WORKSPACE                            |
|                                                               |
|  +-----------+  +-----------+  +-----------+  +-----------+  |
|  | MODULES   |  | TEST CASES|  | EXECUTION |  | REPORTS   |  |
|  |           |  |           |  |  LISTS    |  |           |  |
|  | Reusable  |  | Business  |  |           |  | Pass/Fail |  |
|  | UI/API    |  | scenarios |  | Scheduled |  | Coverage  |  |
|  | building  |  | built from|  | test runs |  | Defects   |  |
|  | blocks    |  | modules   |  |           |  |           |  |
|  +-----------+  +-----------+  +-----------+  +-----------+  |
|                                                               |
|  +-----------+  +-----------+  +-----------+                 |
|  | REQUIRE-  |  | TEST DATA |  | LIBRARY   |                 |
|  | MENTS     |  |           |  |           |                 |
|  |           |  | Excel /   |  | Shared    |                 |
|  | Traceability  TDM / DB   |  | configs   |                 |
|  | coverage  |  | driven    |  | & utils   |                 |
|  +-----------+  +-----------+  +-----------+                 |
+---------------------------------------------------------------+
```

### TOSCA Terminology

| Term | What It Is |
|------|-----------|
| **Repository** | Central database — all test assets live here |
| **Workspace** | Your local checkout from the repository |
| **Module** | A scanned UI component (form, button, field) |
| **TestCase** | A sequence of steps using modules |
| **TestStep** | A single action (click, enter text, verify) |
| **ExecutionList** | An ordered set of test cases to run |
| **ScratchBook** | Personal scratch area — not shared |
| **TestSheet** | Deprecated; use ExecutionList instead |
| **TBox** | TOSCA's test engine — executes test steps |
| **TCI (Commander)** | TOSCA CI — runs tests from command line/CI |
| **Steering** | Parameterizing test steps with values |
| **Buffer** | Temporary storage for captured values |

---

## 3. TOSCA Architecture

### Component Diagram

```
+-------------------------------------------------------------------+
|                     TOSCA ARCHITECTURE                            |
|                                                                   |
|  +------------------+          +------------------+              |
|  |  TOSCA COMMANDER |          |  TOSCA AGENT     |              |
|  |  (Orchestrator)  |<-------->|  (Executor)      |              |
|  |                  |          |                  |              |
|  | - Repository mgmt|          | - Runs TBox      |              |
|  | - Test design    |          | - Controls AUT   |              |
|  | - Scheduling     |          | - Reports results|              |
|  +------------------+          +------------------+              |
|          |                             |                          |
|          v                             v                          |
|  +------------------+          +------------------+              |
|  |   SQL SERVER     |          | APPLICATION      |              |
|  |   REPOSITORY     |          | UNDER TEST (AUT) |              |
|  |                  |          |                  |              |
|  | - Shared assets  |          | Oracle EBS       |              |
|  | - Version control|          | Oracle Forms     |              |
|  | - Multi-user     |          | Oracle Fusion    |              |
|  +------------------+          | Oracle ADF       |              |
|                                +------------------+              |
+-------------------------------------------------------------------+
```

### TOSCA Technology Support

```
+--------------------------------------+
|        TOSCA ENGINE SUPPORT          |
+--------------------------------------+
| WEB           | Chrome, Firefox, Edge |
| DESKTOP       | WPF, WinForms, Java   |
| ORACLE        | EBS, Forms, Fusion,   |
|               | ADF, APEX             |
| SAP           | GUI, Web, Fiori       |
| MOBILE        | iOS, Android          |
| API           | REST, SOAP, GraphQL   |
| DATABASE      | Oracle DB, SQL Server |
| MAINFRAME     | z/OS, AS400           |
| PACKAGED APPS | Salesforce, ServiceNow|
+--------------------------------------+
```

---

## 4. Setting Up TOSCA for Oracle Applications

### Prerequisites

```
REQUIRED COMPONENTS
+-------------------+     +-------------------+     +-------------------+
| TOSCA Commander   |     | Oracle Client     |     | AUT Access        |
| (v14+)            |     | (if Oracle Forms) |     |                   |
| - License file    |     | - Oracle Forms    |     | - Oracle EBS URL  |
| - SQL Server DB   |     |   Plugin enabled  |     | - Test credentials|
| - .NET Framework  |     | - Correct version |     | - Test environment|
+-------------------+     +-------------------+     +-------------------+
```

### Oracle EBS Scanning Setup

TOSCA uses **scanning** to discover UI elements in Oracle apps and create Modules automatically.

```
SCANNING WORKFLOW
+----------------+
| 1. Open TOSCA  |
| Commander      |
+-------+--------+
        |
        v
+-------+--------+
| 2. Open AUT    |
| (Oracle EBS    |
|  in browser)   |
+-------+--------+
        |
        v
+-------+--------+
| 3. TOSCA ->    |
| Modules ->     |
| Scan Application|
+-------+--------+
        |
        v
+-------+--------+
| 4. Highlight   |
| UI elements    |
| to scan        |
+-------+--------+
        |
        v
+-------+--------+
| 5. Module      |
| created with   |
| all controls   |
+----------------+
```

### Oracle-Specific TOSCA Engines

| Oracle Technology | TOSCA Engine | Notes |
|-------------------|-------------|-------|
| Oracle EBS (R12) | TBox Web + Oracle Forms | Requires Oracle Forms plugin |
| Oracle Fusion | TBox Web (Chrome) | Standard web scanning |
| Oracle ADF | TBox Web | Standard web scanning |
| Oracle APEX | TBox Web | Standard web scanning |
| Oracle DB | TBox Database | JDBC connection |
| Oracle Forms (standalone) | TBox Oracle Forms | Dedicated engine |

### Configuring Oracle DB Connection

```
In TOSCA Commander:
1. Right-click [Modules] -> New -> TBox Database Connection
2. Connection properties:
   +------------------------------------------+
   | Provider:     Oracle (ODP.NET)            |
   | Data Source:  //hostname:1521/SERVICENAME  |
   | User ID:      your_db_user                |
   | Password:     your_db_pass                |
   +------------------------------------------+
3. Test connection -> Save
```

---

## 5. Beginner: Your First TOSCA Test

### Step 1: Scan Oracle EBS Login Page

After opening Oracle EBS in a browser:

```
TOSCA Commander
├── Modules (right-click)
│   └── Scan Application
│       └── Scan the following elements:
│           ├── Username field    -> "Username"
│           ├── Password field    -> "Password"
│           └── Login button      -> "Login"
│
Result:
└── [Module] Oracle_EBS_Login
    ├── [ModuleAttribute] Username  {Action: Input}
    ├── [ModuleAttribute] Password  {Action: Input}
    └── [ModuleAttribute] Login_Btn {Action: Click}
```

### Step 2: Create a Test Case

```
TOSCA Commander
└── TestCases
    └── (right-click) -> New TestCase
        └── [TC_001] Login_to_Oracle_EBS
            └── TestSteps:
                ├── [TS_01] Navigate to EBS URL
                │   Module: Browser Actions
                │   Action: OpenURL
                │   Value:  http://your-ebs-server/OA_HTML/AppsLogin
                │
                ├── [TS_02] Enter Username
                │   Module: Oracle_EBS_Login
                │   Attribute: Username
                │   Value: "SYSADMIN"
                │
                ├── [TS_03] Enter Password
                │   Module: Oracle_EBS_Login
                │   Attribute: Password
                │   Value: "sysadmin"   (use encrypted buffer in real tests)
                │
                ├── [TS_04] Click Login
                │   Module: Oracle_EBS_Login
                │   Attribute: Login_Btn
                │   Action: Click
                │
                └── [TS_05] Verify Home Page
                    Module: Oracle_EBS_Home
                    Attribute: Welcome_Text
                    Action: Verify
                    Expected: "Oracle E-Business Suite"
```

### Step 3: Create an Execution List and Run

```
TOSCA Commander
└── ExecutionLists
    └── (right-click) -> New ExecutionList
        └── [EL_Smoke] Smoke_Tests
            └── Drag TC_001 into this list
                |
                v
            Press F6 or click [Run] button
                |
                v
        +----------------------------+
        | EXECUTION RESULT           |
        | TC_001: PASSED ✓           |
        | Duration: 00:00:45         |
        | Steps: 5/5 Passed          |
        +----------------------------+
```

### Beginner Tips

```
DO                                    DON'T
+----------------------------------+  +----------------------------------+
| ✓ Always scan elements fresh     |  | ✗ Hardcode selectors manually   |
| ✓ Use descriptive names          |  | ✗ Name tests "Test1", "Test2"   |
| ✓ Verify after every action      |  | ✗ Skip verification steps        |
| ✓ Use test data files (Excel)    |  | ✗ Hardcode passwords in steps   |
| ✓ Check in to repo often         |  | ✗ Work only in ScratchBook      |
| ✓ Run tests in clean state       |  | ✗ Depend on previous test state |
+----------------------------------+  +----------------------------------+
```

---

## 6. Intermediate: Advanced TOSCA Techniques

### 6.1 Data-Driven Testing with TestSheets / Excel

Instead of one test with hardcoded values, drive tests from data:

```
EXCEL TEST DATA (TestData.xlsx)
+--------+----------+------------------+------------------+
| Row    | Username | Password         | Expected_Result  |
+--------+----------+------------------+------------------+
| 1      | SYSADMIN | sysadmin         | Login Successful |
| 2      | USER1    | Welcome1         | Login Successful |
| 3      | BADUSER  | wrongpass        | Invalid Creds    |
| 4      | ""       | ""               | Please enter user|
+--------+----------+------------------+------------------+

TOSCA reads each row -> runs test once per row
Total: 4 test executions from 1 test case
```

**How to set up:**

```
1. In TOSCA: TestCase -> right-click -> Create TestDataSet
2. Link Excel file: Browse to TestData.xlsx
3. Map columns to TestStep parameters:
   Username  -> {TS_02.Username}
   Password  -> {TS_03.Password}
4. Run: TOSCA iterates all rows automatically
```

### 6.2 Buffers — Capturing Dynamic Values

Oracle apps generate dynamic IDs (PO numbers, invoice IDs). Use Buffers to capture and reuse them:

```
SCENARIO: Create PO -> Verify PO in list

[TS_01] Create Purchase Order
        Action: Click "Save"

[TS_02] Capture PO Number
        Module:  PO_Confirmation_Page
        Attribute: PO_Number_Field
        Action:  READVALUE           <- Reads the generated PO# into buffer
        Buffer:  {B_PO_Number}       <- Stores value here

[TS_03] Navigate to PO Search

[TS_04] Search for captured PO
        Module:  PO_Search_Page
        Attribute: Search_Field
        Action:  Input
        Value:   {B_PO_Number}       <- Reuses captured value

[TS_05] Verify PO exists
        Expected: {B_PO_Number}
```

### 6.3 Modular Test Design — Building Reusable Libraries

```
LIBRARY STRUCTURE (Best Practice)
+--------------------------------------------------+
|  [Modules]                                       |
|    ├── Oracle_Common                             |
|    │   ├── Navigation_Menu                      |
|    │   ├── Search_Bar                           |
|    │   └── Breadcrumb                           |
|    ├── Oracle_Procurement                        |
|    │   ├── PO_Header_Form                       |
|    │   ├── PO_Lines_Table                       |
|    │   └── PO_Approval_Workflow                 |
|    └── Oracle_Finance                            |
|        ├── AP_Invoice_Entry                     |
|        ├── GL_Journal_Entry                     |
|        └── AR_Receipt_Application              |
|                                                  |
|  [TestCases]                                     |
|    ├── Smoke                                    |
|    │   ├── TC_Login_EBS                         |
|    │   └── TC_Navigate_Menus                   |
|    ├── Regression                               |
|    │   ├── TC_Create_PO_Full                   |
|    │   ├── TC_Approve_PO                       |
|    │   └── TC_Receive_Goods                    |
|    └── Integration                              |
|        ├── TC_PO_to_AP_Invoice                 |
|        └── TC_AP_Invoice_to_Payment             |
+--------------------------------------------------+
```

### 6.4 Risk-Based Testing (TOSCA TQL)

TOSCA's **Test Query Language (TQL)** lets you filter execution based on risk/priority:

```
TQL EXAMPLE — Run only HIGH risk tests:

WHERE Risk = "High" AND Status != "Passed"
ORDER BY Priority DESC

Result: Only untested or failing high-risk cases run
        -> Saves time in regression cycles
```

### 6.5 Oracle ADF / Fusion Testing Patterns

```
CHALLENGE: Oracle Fusion pages are dynamic (ADF partial rendering)

SOLUTION PATTERN:
+----------------------------------------------+
| [TS_01] Navigate to Fusion Page              |
|         WaitForDocumentReady = True          |  <- Wait for ADF load
|                                              |
| [TS_02] Click search button                  |
|         WaitForDocumentReady = True          |  <- Wait for results
|                                              |
| [TS_03] Handle ADF popups                   |
|         Use: ADF Popup Handler module        |
|                                              |
| [TS_04] Scroll-to-element before interact   |
|         Action: ScrollIntoView              |
+----------------------------------------------+

KEY SETTINGS for Oracle ADF:
- Engine: TBox Web
- Frame Handling: Auto
- Synchronization: WaitForDocumentReady
- Timeouts: Increase to 60s+ for heavy pages
```

### 6.6 API Testing in TOSCA

Test Oracle REST APIs (used in Fusion/APEX) directly:

```
[TC] Test_Oracle_REST_API_Create_PO

[TS_01] POST to Oracle REST API
        Engine:  TBox APIEngine
        Method:  POST
        URL:     https://oracle-fusion/fscmRestApi/resources/v11.13.18.05/purchaseOrders
        Headers:
          Authorization: Basic {Buffer_Auth_Token}
          Content-Type:  application/json
        Body:
          {
            "BuyerName": "John Smith",
            "Description": "Test PO via API",
            "Lines": [...]
          }

[TS_02] Verify Response Status
        Assert: StatusCode == 201

[TS_03] Capture PO Number from Response
        JsonPath: $.OrderNumber
        Buffer:   {B_API_PO_Number}

[TS_04] Verify PO in UI (cross-channel check)
        Use: UI module to search for {B_API_PO_Number}
```

### 6.7 TOSCA Git Integration

TOSCA workspaces can be stored in Git for version control:

```
TOSCA + GIT WORKFLOW
+-------------------+
| Developer commits |
| Oracle app changes|
+--------+----------+
         |
         v (triggers Jenkins)
+--------+----------+
| Jenkins pulls     |
| latest TOSCA tests|
| from Git repo     |
+--------+----------+
         |
         v
+--------+----------+
| TOSCA CI executes |
| regression suite  |
+--------+----------+
         |
         v
+--------+----------+
| Results -> JIRA   |
| Zephyr defects    |
| logged auto       |
+-------------------+
```

---

## 7. Jenkins Basics & TOSCA Integration

### What Is Jenkins?

Jenkins is an open-source **Continuous Integration / Continuous Delivery (CI/CD)** automation server. It triggers automated tests (including TOSCA) on every code change.

```
JENKINS CI/CD PIPELINE
+----------+   +----------+   +----------+   +----------+   +----------+
|  CODE    |-->|  BUILD   |-->|   TEST   |-->|  STAGE   |-->|  DEPLOY  |
|  COMMIT  |   |          |   |          |   |          |   |          |
| Dev pushes   | Compile  |   | TOSCA    |   | Deploy   |   | Deploy   |
| to Git   |   | package  |   | runs     |   | to test  |   | to prod  |
|          |   | artifact |   | regression   | env      |   |          |
+----------+   +----------+   +----------+   +----------+   +----------+
                                   ^
                              [YOU ARE HERE]
                              TOSCA integrates
                              at this stage
```

### Jenkins Core Concepts

| Concept | Description |
|---------|-------------|
| **Job / Project** | A configured task (build, test, deploy) |
| **Pipeline** | A series of stages defined as code (Jenkinsfile) |
| **Stage** | A logical phase in a pipeline (Build, Test, Deploy) |
| **Step** | A single command or action within a stage |
| **Agent/Node** | The machine that executes jobs |
| **Trigger** | What starts a job (push, schedule, manual) |
| **Artifact** | Output files saved from a job |
| **Plugin** | Extensions that add functionality |

### Jenkins Pipeline Syntax (Jenkinsfile)

```groovy
// Jenkinsfile — TOSCA Oracle Regression Pipeline
pipeline {
    agent any

    environment {
        TOSCA_COMMANDER = "C:\\Program Files\\TOSCA\\Commander"
        TOSCA_REPO      = "C:\\TOSCA\\OracleEBS_Repo"
        EXECUTION_LIST  = "Regression_Suite"
    }

    triggers {
        // Run every night at 11 PM
        cron('0 23 * * 1-5')
        // Also run on Oracle EBS code push
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-org/oracle-tests.git'
            }
        }

        stage('Update TOSCA Workspace') {
            steps {
                bat """
                    ToscaCI.exe update-workspace ^
                        --workspace ${TOSCA_REPO}
                """
            }
        }

        stage('Run TOSCA Tests') {
            steps {
                bat """
                    ToscaCI.exe run ^
                        --workspace ${TOSCA_REPO} ^
                        --executionList "${EXECUTION_LIST}" ^
                        --resultFile results\\tosca-results.xml
                """
            }
            post {
                always {
                    // Publish test results to Jenkins
                    junit 'results\\tosca-results.xml'
                }
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML([
                    reportDir: 'results',
                    reportFiles: 'TOSCA_Report.html',
                    reportName: 'TOSCA Test Report'
                ])
            }
        }
    }

    post {
        failure {
            // Notify team on failure
            emailext(
                to: 'qa-team@yourorg.com',
                subject: "Oracle EBS Regression FAILED - Build ${BUILD_NUMBER}",
                body: "See: ${BUILD_URL}"
            )
        }
        success {
            echo 'All Oracle EBS tests passed!'
        }
    }
}
```

### TOSCA CI (ToscaCI.exe) Commands

```
TOSCA CI Command Reference:

# Run an ExecutionList
ToscaCI.exe run
  --workspace   "C:\TOSCA\OracleEBS_Repo"
  --executionList "Regression_Suite"
  --resultFile  "results\results.xml"
  --importResults True

# Update workspace from repository
ToscaCI.exe update-workspace
  --workspace "C:\TOSCA\OracleEBS_Repo"

# Import results back to TOSCA
ToscaCI.exe import-results
  --workspace "C:\TOSCA\OracleEBS_Repo"
  --resultFile "results\results.xml"

# Run with specific test config
ToscaCI.exe run
  --workspace   "..."
  --executionList "Smoke"
  --parameter   "Environment=QA"
  --parameter   "Browser=Chrome"
```

### Jenkins + TOSCA Setup Checklist

```
SETUP CHECKLIST
+---+------------------------------------------+
| ✓ | Install Jenkins on CI server             |
| ✓ | Install TOSCA Commander + ToscaCI on     |
|   | same CI server (or agent)                |
| ✓ | Configure Jenkins agent as TOSCA machine |
| ✓ | Add TOSCA plugin to Jenkins              |
|   | (Tricentis Continuous Integration plugin)|
| ✓ | Create Jenkins credentials for TOSCA repo|
| ✓ | Create Jenkinsfile in your test repo     |
| ✓ | Configure webhook: Oracle repo -> Jenkins|
| ✓ | Test: manually trigger pipeline          |
| ✓ | Verify: results appear in Jenkins UI     |
| ✓ | Configure notifications (email/Slack)    |
+---+------------------------------------------+
```

---

## 8. Zephyr Basics & Test Management

### What Is Zephyr?

**Zephyr** is a test management tool, most commonly used as a **JIRA plugin** (Zephyr Scale / Zephyr Squad). It organizes test cases, test plans, test cycles, and links them to JIRA issues.

```
ZEPHYR IN THE ECOSYSTEM
+--------+    +---------+    +---------+    +---------+
| JIRA   |    | ZEPHYR  |    | TOSCA   |    | JENKINS |
|        |    |         |    |         |    |         |
| Stories+<-->+ Test    +<-->+ Test    +<-->+ Runs    |
| Bugs   |    | Cases   |    | Execution    | TOSCA   |
| Epics  |    | Plans   |    | Results |    | pushes  |
|        |    | Cycles  |    | sync'd  |    | results |
+--------+    +---------+    +---------+    +---------+
```

### Zephyr Core Concepts

| Term | Description |
|------|-------------|
| **Test Case** | A documented test scenario in Zephyr |
| **Test Plan** | High-level: what to test for a release/sprint |
| **Test Cycle** | A scheduled execution run for a test plan |
| **Test Execution** | Running a specific test case in a cycle |
| **Traceability** | Linking test cases to JIRA requirements |
| **Coverage** | % of stories/epics covered by test cases |
| **Folder** | Organizing structure for test cases |
| **Component** | Grouping by feature/module |

### Zephyr Hierarchy

```
ZEPHYR STRUCTURE
+-------------------------------------------+
| PROJECT: Oracle EBS Implementation         |
|                                           |
|   TEST PLAN: Release 3.2                  |
|   |                                       |
|   +-- TEST CYCLE: Sprint 14 Regression    |
|   |   |                                   |
|   |   +-- EXECUTION: TC-101 Login         |
|   |   |   Status: PASSED                  |
|   |   |   Assignee: QA Engineer           |
|   |   |                                   |
|   |   +-- EXECUTION: TC-102 Create PO     |
|   |   |   Status: FAILED                  |
|   |   |   Defect: BUG-445 (auto-linked)   |
|   |   |                                   |
|   |   +-- EXECUTION: TC-103 Approve PO    |
|   |       Status: IN PROGRESS             |
|   |                                       |
|   +-- TEST CYCLE: Sprint 14 Smoke         |
|       (subset of critical tests)          |
+-------------------------------------------+
```

### Writing Good Test Cases in Zephyr

```
TEST CASE TEMPLATE
+-------------------------------------------+
| ID:          TC-101                       |
| Name:        Login to Oracle EBS          |
| Component:   Authentication               |
| Priority:    High                         |
| Req. Link:   REQ-001 (JIRA story)         |
+-------------------------------------------+
| PRECONDITIONS:                            |
| - Oracle EBS is accessible               |
| - Test user SYSADMIN exists              |
| - Browser: Chrome latest                 |
+-------------------------------------------+
| TEST STEPS:                               |
| Step | Action              | Expected      |
|------|---------------------|---------------|
|  1   | Navigate to EBS URL | Login page    |
|      |                     | displayed     |
|  2   | Enter "SYSADMIN"    | Text appears  |
|      | in Username field   | in field      |
|  3   | Enter password      | Masked chars  |
|  4   | Click Login button  | Home page     |
|      |                     | displayed     |
|  5   | Verify welcome text | "Welcome,     |
|      |                     | SYSADMIN"     |
+-------------------------------------------+
| POSTCONDITIONS:                           |
| - User is logged in                       |
| - Session is active                       |
+-------------------------------------------+
```

### Zephyr + TOSCA Integration

TOSCA can automatically sync execution results to Zephyr:

```
INTEGRATION FLOW
+---------------+     +---------------+     +---------------+
| TOSCA         |     | TOSCA ZEPHYR  |     | ZEPHYR/JIRA   |
| Executes Test |---->| Integration   |---->| Updates Test  |
|               |     | Plugin        |     | Execution     |
| Result:       |     |               |     | Status:       |
| TC-101 PASSED |     | Maps by       |     | TC-101 PASSED |
| TC-102 FAILED |     | test ID       |     | TC-102 FAILED |
|               |     |               |     | Bug auto-     |
|               |     |               |     | created       |
+---------------+     +---------------+     +---------------+
```

**Configuration in TOSCA:**

```
TOSCA Commander -> Settings -> Defect Tracking
  +----------------------------------------------+
  | Type:    Jira                                |
  | URL:     https://your-org.atlassian.net      |
  | Project: ORACLE_EBS                          |
  | Username: tosca-service@yourorg.com          |
  | API Token: [your-jira-api-token]             |
  +----------------------------------------------+

Result: Failed tests auto-create JIRA bugs
        linked to Zephyr test executions
```

### Zephyr Reporting Metrics

```
KEY METRICS TO TRACK
+---------------------------------------------+
| EXECUTION STATUS                            |
|                                             |
|  Passed  [====================] 65% (65)    |
|  Failed  [======]              20% (20)     |
|  Blocked [===]                 10% (10)     |
|  In Prog [=]                    5%  (5)     |
|  Total:                       100  tests    |
+---------------------------------------------+
| REQUIREMENT COVERAGE                        |
|                                             |
|  Covered   [================]   80% (40 req)|
|  Uncovered [====]               20% (10 req)|
+---------------------------------------------+
| DEFECT DENSITY                              |
|  Defects per feature module                 |
|  Procurement: ████████ 8 bugs               |
|  Finance:     █████ 5 bugs                  |
|  HR:          ██ 2 bugs                     |
+---------------------------------------------+
```

---

## 9. End-to-End Workflow

### Full Oracle EBS Testing Pipeline

```
+------------------------------------------------------------------+
|              END-TO-END TOSCA ORACLE WORKFLOW                    |
+------------------------------------------------------------------+

  BUSINESS ANALYST          QA ENGINEER             CI/CD
  +-----------------+       +-----------------+     +-----------------+
  | Write user      |       | Create test     |     | Dev commits     |
  | stories in JIRA |       | cases in Zephyr |     | Oracle code     |
  +-----------------+       | linked to JIRA  |     +-----------------+
          |                 | stories         |             |
          |                 +-----------------+             |
          |                         |                       |
          v                         v                       v
  +-----------------+       +-----------------+     +-----------------+
  | Sign off on     |       | Build TOSCA     |     | Jenkins webhook |
  | requirements    |       | modules from    |     | triggered       |
  +-----------------+       | Oracle EBS scan |     +-----------------+
                            +-----------------+             |
                                    |                       v
                                    v               +-----------------+
                            +-----------------+     | TOSCA CI runs   |
                            | Create TOSCA    |     | ExecutionList   |
                            | test cases      |     | on agent        |
                            | using modules   |     +-----------------+
                            +-----------------+             |
                                                           v
                                                  +-----------------+
                                                  | Results sync to |
                                                  | Zephyr cycles   |
                                                  +-----------------+
                                                           |
                                                           v
                                                  +-----------------+
                                                  | Failures ->     |
                                                  | JIRA bugs auto  |
                                                  | created         |
                                                  +-----------------+
                                                           |
                                                           v
                                                  +-----------------+
                                                  | Jenkins builds  |
                                                  | report + notif  |
                                                  | to QA team      |
                                                  +-----------------+
```

---

## 10. Cheat Sheet & Quick Reference

### TOSCA Keyboard Shortcuts

```
+-----------------------------+---------------------------+
| ACTION                      | SHORTCUT                  |
+-----------------------------+---------------------------+
| New TestCase                | Ctrl+N (in TC section)    |
| Run TestCase                | F6                        |
| Check in to repository      | Ctrl+S then Ctrl+Shift+I  |
| Update workspace            | Ctrl+Shift+U              |
| Open Properties             | F4                        |
| Scan Application            | Ctrl+Shift+S              |
| Open Module search          | Ctrl+F                    |
| Expand all                  | Ctrl+Shift+E              |
| Collapse all                | Ctrl+Shift+C              |
+-----------------------------+---------------------------+
```

### TOSCA Action Types Reference

```
+------------------+------------------------------------------+
| ACTION           | USE CASE                                 |
+------------------+------------------------------------------+
| Input            | Type text into a field                   |
| Click            | Click a button or link                   |
| Check            | Select a checkbox                        |
| Select           | Choose from dropdown                     |
| Verify           | Assert field value matches expected      |
| VerifyExists     | Assert element is present on page        |
| ReadValue        | Capture field value into buffer          |
| ScrollIntoView   | Scroll element into visible area         |
| WaitForObject    | Pause until element appears              |
| KeyStroke        | Press keyboard key (Tab, Enter, F4...)   |
+------------------+------------------------------------------+
```

### Common Oracle EBS Test Scenarios Checklist

```
ORACLE EBS REGRESSION SUITE - COMMON SCENARIOS

[ ] AUTHENTICATION
    [ ] Valid login
    [ ] Invalid credentials
    [ ] Session timeout
    [ ] Password reset

[ ] PROCUREMENT (PO Module)
    [ ] Create standard PO
    [ ] Create blanket PO
    [ ] Add PO lines (items/services)
    [ ] Submit PO for approval
    [ ] Approve PO (approval workflow)
    [ ] Receive goods against PO

[ ] ACCOUNTS PAYABLE
    [ ] Create supplier invoice
    [ ] Match invoice to PO
    [ ] Validate invoice
    [ ] Pay invoice
    [ ] On-hold invoice handling

[ ] ACCOUNTS RECEIVABLE
    [ ] Create customer invoice
    [ ] Apply receipt to invoice
    [ ] Credit memo creation

[ ] GENERAL LEDGER
    [ ] Journal entry creation
    [ ] Journal approval
    [ ] Period close process

[ ] HR / PAYROLL (if applicable)
    [ ] Employee hire
    [ ] Salary update
    [ ] Payroll run
```

### Troubleshooting Quick Guide

```
ISSUE                         |  SOLUTION
------------------------------|------------------------------------------
Element not found             |  Re-scan module; check if Oracle page
                              |  changed after patch; increase timeout
Test passes manually,         |  Add WaitForDocumentReady; check if
fails in TOSCA               |  ADF partial rendering is complete
Oracle login popup appearing  |  Add browser credential handler module;
unexpectedly                  |  or pre-configure browser profile
Buffer value is empty         |  Verify ReadValue action is correct;
                              |  check element has visible text
Jenkins job not triggering    |  Check webhook config; verify Jenkinsfile
                              |  syntax; check Jenkins agent is online
Zephyr not updating           |  Check API token expiry; verify project
                              |  key mapping in TOSCA settings
```

### Glossary

```
AUT   = Application Under Test
TBox  = TOSCA's test execution engine
TCI   = TOSCA Continuous Integration (CLI tool)
TQL   = Test Query Language (TOSCA's filter language)
EBS   = E-Business Suite (Oracle's legacy ERP)
ADF   = Application Development Framework (Oracle UI tech)
CI/CD = Continuous Integration / Continuous Delivery
EL    = ExecutionList (TOSCA test run container)
```

---

## Resources & Next Steps

```
LEARNING PATH - NEXT STEPS
+--------------------------------------------+
| BEGINNER (You are here ✓)                  |
|  ✓ Install TOSCA trial                     |
|  ✓ Scan a simple Oracle form               |
|  ✓ Create 5 basic test cases               |
|  ✓ Run your first ExecutionList            |
+--------------------------------------------+
         |
         v
+--------------------------------------------+
| INTERMEDIATE                               |
|  → Build reusable module library           |
|  → Implement data-driven tests             |
|  → Set up Jenkins pipeline                 |
|  → Connect Zephyr to JIRA                  |
|  → Write API tests for Oracle REST         |
+--------------------------------------------+
         |
         v
+--------------------------------------------+
| ADVANCED                                   |
|  → Risk-based test optimization (TQL)      |
|  → Parallel distributed test execution     |
|  → TOSCA DIV (distributed test)           |
|  → Custom TBox development                 |
|  → TOSCA + ServiceNow/Snowflake integration|
+--------------------------------------------+
```

**Official Resources:**
- Tricentis Documentation: https://documentation.tricentis.com/tosca/
- Tricentis Academy (free courses): https://academy.tricentis.com/
- TOSCA Community: https://community.tricentis.com/
- Zephyr Scale Docs: https://support.smartbear.com/zephyr-scale-cloud/docs/
- Jenkins Docs: https://www.jenkins.io/doc/

---

*Guide created for Oracle EBS/Fusion testing teams — covers TOSCA automation from first scan to CI/CD pipeline integration.*
