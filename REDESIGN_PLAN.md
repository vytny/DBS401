# CTF Lab Redesign Plan - Database Security

## Mục Tiêu Redesign

Tái cấu trúc CTF lab theo chuẩn pentest workflow và tối ưu cho sinh viên năm 4, thời gian lab nửa ngày - 1 ngày.

## New Pentest Workflow

```
RECONNAISSANCE (30 min)
    ↓
MISCONFIGURATION DISCOVERY (45 min)
    ↓
PRIVILEGE ESCALATION (1 hour)
    ↓
INJECTION ATTACKS (1.5 hours)
    ↓
KEY EXTRACTION (45 min)
```

**Total: ~4.5 hours** (comfortable for half-day to full-day lab)

---

## 10 Challenges Redesign

### PHASE 1: RECONNAISSANCE (200 points)

#### Challenge 1: Network Scanning & Port Discovery (100 pts)
**Learning Objectives:**
- Sử dụng nmap để scan network
- Hiểu về service fingerprinting
- Identify open ports và services

**Tools:** nmap, netcat
**AI Assistance:** ChatGPT để explain nmap flags
**Estimated Time:** 15 minutes

**Flag Location:** system_info table, column 'service_banner'
**Key Skill:** Basic network reconnaissance

---

#### Challenge 2: Database Version & Banner Grabbing (100 pts)
**Learning Objectives:**
- Connect MySQL client
- Extract version information
- Understand database fingerprinting

**Tools:** mysql client, telnet
**AI Assistance:** Claude để parse MySQL banner
**Estimated Time:** 15 minutes

**Flag Location:** system_info table, column 'db_version'
**Key Skill:** Service enumeration

---

### PHASE 2: MISCONFIGURATION DISCOVERY (400 points)

#### Challenge 3: Weak Credentials Discovery (100 pts)
**Learning Objectives:**
- Hiểu về default credentials
- Test common username/password combinations
- Use wordlist attacks

**Tools:** hydra, custom Python script
**AI Assistance:** Generate wordlist với ChatGPT
**Estimated Time:** 15 minutes

**Flag Location:** Successfully login với weak credentials → flag in welcome message
**Misconfiguration:** User 'backup'@'%' with password 'backup123'

---

#### Challenge 4: Excessive Privileges Detection (150 pts)
**Learning Objectives:**
- Query mysql.user table
- Identify users with dangerous privileges (FILE, SUPER)
- Understand principle of least privilege

**Tools:** MySQL queries
**AI Assistance:** AI explain privilege implications
**Estimated Time:** 15 minutes

**Flag Location:** User comments containing flag
```sql
SELECT User, Host, File_priv, Super_priv FROM mysql.user;
```

**Misconfiguration:** User 'ctf_user' has FILE privilege (can read files)

---

#### Challenge 5: Insecure Configuration Audit (150 pts)
**Learning Objectives:**
- Check MySQL configuration variables
- Identify security misconfigurations
- Understand secure_file_priv, local_infile

**Tools:** MySQL SHOW VARIABLES
**AI Assistance:** AI audit configuration dump
**Estimated Time:** 15 minutes

**Flag Location:** Variable comments or config_audit table
```sql
SHOW VARIABLES LIKE '%secure_file%';
SHOW VARIABLES LIKE '%local_infile%';
```

**Misconfiguration:** secure_file_priv = "" (can read any file)

---

### PHASE 3: PRIVILEGE ESCALATION (450 points)

#### Challenge 6: Horizontal Privilege Escalation (200 pts)
**Learning Objectives:**
- Access data của users khác
- Exploit weak access controls
- Understand IDOR vulnerabilities

**Tools:** SQL queries, Burp Suite
**AI Assistance:** Generate SQL queries để enumerate users
**Estimated Time:** 30 minutes

**Flag Location:** Other user's profile/data
```sql
SELECT * FROM users WHERE id != current_user_id;
```

**Technique:** UNION-based injection để access other user data

---

#### Challenge 7: Vertical Privilege Escalation via Stored Procedures (250 pts)
**Learning Objectives:**
- Enumerate stored procedures
- Call admin-only procedures
- Understand SQL injection in stored procedures

**Tools:** MySQL client, sqlmap
**AI Assistance:** AI explain procedure security model
**Estimated Time:** 30 minutes

**Flag Location:** Output of admin-only procedure
```sql
SHOW PROCEDURE STATUS WHERE Db = 'ctf_database';
CALL get_admin_flag();
```

**Misconfiguration:** Stored procedure with DEFINER=root allows execution by low-priv user

---

### PHASE 4: INJECTION ATTACKS (500 points)

#### Challenge 8: Authentication Bypass (200 pts)
**Learning Objectives:**
- Classic SQL injection
- Bypass login forms
- Understand input validation failures

**Tools:** Burp Suite, manual injection
**AI Assistance:** ChatGPT generate SQLi payloads
**Estimated Time:** 30 minutes

**Flag Location:** Admin panel after successful bypass
**Payload Example:**
```
username: admin' OR '1'='1' --
password: anything
```

**Vulnerability:** No prepared statements in login.php

---

#### Challenge 9: Blind SQL Injection & Data Exfiltration (300 pts)
**Learning Objectives:**
- Boolean-based blind SQLi
- Time-based blind SQLi
- Automated exploitation with scripts

**Tools:** sqlmap, custom Python script with AI
**AI Assistance:** AI optimize blind SQLi script
**Estimated Time:** 1 hour

**Flag Location:** Hidden column in products table
**Payload Example:**
```
id=1 AND (SELECT SUBSTRING(hidden_flag,1,1) FROM products WHERE id=1)='F'
```

**Technique:** Binary search với AI để speed up extraction

---

### PHASE 5: KEY EXTRACTION (250 points)

#### Challenge 10: Master Key via File Read + Log Analysis (250 pts)
**Learning Objectives:**
- Combine multiple techniques
- Use LOAD_FILE() to read sensitive files
- Analyze audit logs
- Piece together final master key

**Tools:** MySQL LOAD_FILE(), log analysis
**AI Assistance:** AI correlate log entries và file contents
**Estimated Time:** 45 minutes

**Flag Location:** Reconstructed from multiple sources:
1. Part 1: Read from `/etc/mysql/secret_part1.txt` via LOAD_FILE()
2. Part 2: Decode from audit_log table
3. Part 3: Extract from trigger definition
4. Combine: FLAG{part1_part2_part3}

**Technique:** Multi-stage exploitation combining:
- File read (FILE privilege)
- Log analysis
- Trigger enumeration

**Final Challenge:** Requires understanding của toàn bộ lab

---

## AI Integration Examples

### 1. AI-Assisted Wordlist Generation
```python
# ai-helpers/generate_wordlist.py
import openai

def generate_mysql_wordlist():
    prompt = """Generate 20 common MySQL default passwords including:
    - Empty password
    - Same as username
    - Common patterns (admin123, password, etc.)
    """
    # Call OpenAI API
    # Return wordlist
```

### 2. AI-Powered Blind SQLi Optimizer
```python
# ai-helpers/blind_sqli_ai.py
def optimize_payload(response_time, current_char):
    prompt = f"""Current blind SQLi:
    - Response time: {response_time}ms
    - Testing char: {current_char}

    Suggest next optimal character to test based on frequency analysis.
    """
    # AI suggests next character
    # Binary search optimization
```

### 3. AI Configuration Auditor
```python
# ai-helpers/config_auditor.py
def audit_mysql_config(config_dump):
    prompt = f"""Audit this MySQL configuration for security issues:
    {config_dump}

    Identify misconfigurations and explain risks.
    """
    # AI analyzes and explains
```

---

## New File Structure

```
database-security-ctf/
├── ai-helpers/                    # NEW: AI integration tools
│   ├── generate_wordlist.py
│   ├── blind_sqli_ai.py
│   ├── config_auditor.py
│   ├── payload_generator.py
│   └── requirements.txt
│
├── solutions/                     # NEW: For instructors
│   ├── INSTRUCTOR_GUIDE.md
│   ├── challenge_01_solution.md
│   ├── challenge_02_solution.md
│   ├── ... (10 solutions)
│   └── grading_rubric.xlsx
│
├── student-materials/             # NEW: Student handouts
│   ├── LAB_MANUAL.md
│   ├── TOOLS_SETUP.md
│   ├── AI_USAGE_GUIDE.md
│   └── REPORT_TEMPLATE.md
│
├── mysql/
│   ├── init/
│   │   ├── 01-schema.sql         # UPDATED: New misconfigurations
│   │   ├── 02-flags.sql          # UPDATED: New flag locations
│   │   └── 03-misconfig.sql      # NEW: Intentional misconfigurations
│   └── my.cnf                     # UPDATED: More realistic weak config
│
├── ctf-platform/
│   ├── app.py                     # UPDATED: New challenge definitions
│   └── templates/
│       └── learning_objectives.html  # NEW: Show learning goals
│
└── flag-generator/
    └── generate_flags.py          # UPDATED: New flag injection logic
```

---

## Implementation Priority

### Week 1: Core Restructuring
1. ✅ Update challenge definitions in app.py
2. ✅ Redesign flag injection logic
3. ✅ Update database schema with new misconfigurations

### Week 2: AI Integration
4. ✅ Create ai-helpers/ folder with 4 example scripts
5. ✅ Add OpenAI API integration examples
6. ✅ Document AI usage in challenges

### Week 3: Educational Materials
7. ✅ Write instructor guide with solutions
8. ✅ Create student lab manual
9. ✅ Design grading rubric

### Week 4: Testing & Documentation
10. ✅ End-to-end testing
11. ✅ Update all documentation
12. ✅ Create demo video

---

## Learning Objectives by Phase

### Phase 1: Reconnaissance
- Students learn basic network scanning
- Understand service fingerprinting
- Practice information gathering

### Phase 2: Misconfiguration Discovery
- Identify common database misconfigurations
- Understand security best practices (by seeing violations)
- Learn privilege enumeration

### Phase 3: Privilege Escalation
- Horizontal vs vertical escalation
- Exploit access control failures
- Understand stored procedure security

### Phase 4: Injection Attacks
- Master SQL injection techniques
- Practice blind SQLi automation
- Combine manual + automated approaches

### Phase 5: Key Extraction
- Synthesize all learned techniques
- Solve complex multi-stage challenges
- Practice reporting and documentation

---

## Grading Rubric (Total: 100 points)

| Category | Points | Criteria |
|----------|--------|----------|
| **Challenges Completed** | 40 | 4 points per challenge (10 total) |
| **Methodology** | 20 | Followed pentest phases correctly |
| **AI Integration** | 15 | Used AI tools effectively |
| **Documentation** | 15 | Clear writeup with screenshots |
| **Time Management** | 10 | Completed within time limit |

**Bonus:** +10 points for discovering unintended solutions or additional vulnerabilities

---

## Success Metrics

Students should be able to:
- [ ] Complete at least 7/10 challenges in 4-5 hours
- [ ] Use at least 2 AI tools during the lab
- [ ] Write a professional pentest report
- [ ] Explain each vulnerability and mitigation
- [ ] Demonstrate understanding of pentest methodology

---

## Next Steps

1. Review and approve this redesign plan
2. Begin implementation phase-by-phase
3. Test with pilot group of students
4. Iterate based on feedback

**Estimated Implementation Time:** 2-3 weeks (parallel work on different components)
