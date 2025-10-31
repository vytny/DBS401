# Project Structure Overview

## 📁 Complete File Structure

```
database-security-ctf/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick start guide (5 minutes)
├── 📄 PENTESTING_GUIDE.md          # Complete pentesting guide
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 LICENSE                      # MIT License + Educational disclaimer
├── 📄 .gitignore                   # Git ignore rules
│
├── 🐳 docker-compose.yml           # Docker orchestration
├── 🔧 setup.bat                    # Windows setup script
│
├── 🔐 .env                         # Environment variables (auto-generated, gitignored)
├── 🏁 flags.json                   # Generated flags (auto-generated, gitignored)
│
├── 📂 flag-generator/              # Flag Generation System
│   └── generate_flags.py           # Python script to generate unique flags
│
├── 📂 mysql/                       # MySQL Database Container
│   ├── Dockerfile                  # MySQL Docker image
│   ├── my.cnf                      # MySQL config (intentionally weak)
│   └── init/                       # Database initialization
│       ├── 01-schema.sql           # Database schema
│       └── 02-flags.sql            # Flag injection (auto-generated)
│
├── 📂 vulnerable-web/              # Vulnerable PHP Web Application
│   ├── Dockerfile                  # PHP-Apache Docker image
│   └── app/                        # Application files
│       ├── index.php               # Main entry point
│       ├── config.php              # Configuration
│       ├── db.php                  # Database functions (VULNERABLE)
│       ├── style.css               # Global styles
│       ├── logout.php              # Logout handler
│       └── pages/                  # Application pages
│           ├── home.php            # Homepage
│           ├── login.php           # Login page (SQLi vulnerable)
│           ├── admin.php           # Admin panel (SQLi vulnerable)
│           ├── products.php        # Products listing
│           ├── product_detail.php  # Product details (SQLi vulnerable)
│           ├── search.php          # Search page (SQLi vulnerable)
│           └── profile.php         # User profile
│
└── 📂 ctf-platform/                # CTF Platform (Flask)
    ├── Dockerfile                  # Python Flask Docker image
    ├── requirements.txt            # Python dependencies
    ├── app.py                      # Main Flask application
    ├── templates/                  # HTML templates
    │   ├── base.html               # Base template
    │   ├── index.html              # Main dashboard
    │   ├── challenge.html          # Individual challenge page
    │   ├── scoreboard.html         # Progress tracking
    │   ├── about.html              # About & instructions
    │   └── 404.html                # 404 page
    └── static/                     # Static assets
        ├── css/
        │   └── style.css           # Main stylesheet
        └── js/
            └── main.js             # JavaScript functionality
```

## 📊 File Statistics

| Component | Files | Description |
|-----------|-------|-------------|
| Documentation | 5 | README, guides, license |
| Configuration | 3 | Docker, setup script, gitignore |
| Flag Generator | 1 | Python script |
| MySQL | 4 | Dockerfile, config, SQL scripts |
| Vulnerable Web | 11 | PHP application with SQLi |
| CTF Platform | 11 | Flask web application |
| **TOTAL** | **35** | Complete CTF environment |

## 🎯 Key Components

### 1. Flag Generation System
**Files:** `flag-generator/generate_flags.py`
- Generates unique flags per instance
- Creates `.env` with random passwords
- Produces `flags.json` for validation
- Injects flags into SQL scripts

**Auto-generated files:**
- `.env` - Environment variables
- `flags.json` - Flag definitions
- `mysql/init/02-flags.sql` - SQL injection script

### 2. MySQL Database
**Files:** `mysql/*`
- Intentionally vulnerable configuration
- 10+ tables with sample data
- Stored procedures, triggers
- Flags hidden in various locations

**Vulnerabilities:**
- No input sanitization
- Weak authentication
- File read permissions
- Information disclosure

### 3. Vulnerable Web Application
**Files:** `vulnerable-web/app/*`
- PHP 8.1 with Apache
- Multiple SQL injection points
- Debug mode enabled
- Error disclosure

**Vulnerable Pages:**
- `/index.php?page=login` - Auth bypass
- `/index.php?page=admin` - Admin SQLi
- `/index.php?page=search` - Search SQLi
- `/index.php?page=product_detail&id=X` - Blind SQLi

### 4. CTF Platform
**Files:** `ctf-platform/*`
- Python Flask application
- 10 challenge definitions
- Flag validation system
- Score tracking
- Hints system

**Features:**
- Challenge dashboard
- Individual challenge pages
- Progress tracking
- Scoreboard
- About page with instructions

## 🔄 Workflow

```
User runs setup.bat
    ↓
generate_flags.py creates:
    • .env (passwords)
    • flags.json (flag definitions)
    • 02-flags.sql (flag injection)
    ↓
Docker Compose builds:
    • MySQL container (port 3306)
    • Vulnerable Web container (port 8080)
    • CTF Platform container (port 5000)
    ↓
User accesses CTF Platform
    ↓
User performs pentesting
    ↓
User submits flags
    ↓
Platform validates against flags.json
    ↓
Score tracked in session
```

## 🎨 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                       USER                              │
└────┬──────────────────┬──────────────────┬─────────────┘
     │                  │                  │
     │ pentest          │ submit flags     │ view app
     │                  │                  │
┌────▼─────────┐  ┌────▼─────────┐  ┌────▼─────────┐
│   MySQL      │  │ CTF Platform │  │ Vulnerable   │
│   :3306      │  │   :5000      │  │ Web :8080    │
│              │  │              │  │              │
│ • ctf_db     │  │ • Flask app  │  │ • PHP app    │
│ • flags      │  │ • Validate   │  │ • SQLi vuln  │
│ • vuln cfg   │  │ • Scoring    │  │ • Debug mode │
└──────────────┘  └──────────────┘  └──────────────┘
     ▲                  ▲                  ▲
     │                  │                  │
     └──────────────────┴──────────────────┘
                Docker Network
```

## 🔐 Security by Design

### Intentional Vulnerabilities:
1. **SQL Injection** - Multiple injection points
2. **Information Disclosure** - Debug mode, error messages
3. **Weak Configuration** - MySQL settings
4. **Authentication Bypass** - SQLi in login
5. **Privilege Issues** - Excessive grants
6. **File Reading** - LOAD_FILE enabled

### Protected Elements:
- CTF Platform has no vulnerabilities
- Flag validation is secure
- Session management proper
- No actual malicious code

## 📦 Dependencies

### Python (Flag Generator & CTF Platform):
```
Flask==3.0.0
Flask-Session==0.5.0
PyMySQL==1.1.0
python-dotenv==1.0.0
cryptography==41.0.7
Werkzeug==3.0.1
```

### Docker Images:
- `mysql:8.0` - Base MySQL image
- `php:8.1-apache` - PHP with Apache
- `python:3.11-slim` - Python runtime

## 🎯 Challenge Mapping

| Challenge | Location | Flag Storage |
|-----------|----------|--------------|
| 1. DB Fingerprinting | MySQL | system_info table |
| 2. Service Enum | MySQL | system_info table |
| 3. Schema Discovery | MySQL | Hidden database name |
| 4. User Enum | MySQL | User comments |
| 5. Auth Bypass | Web App | admin_panel table |
| 6. Blind SQLi | Web App | products.hidden_flag |
| 7. File Read | MySQL | file_references table |
| 8. Priv Escalation | MySQL | Stored procedure |
| 9. Backdoor | MySQL | Trigger definition |
| 10. Log Analysis | MySQL | audit_log table |

## 🚀 Deployment

### Development:
```bash
docker-compose up -d
```

### Production (NOT RECOMMENDED):
⚠️ **DO NOT deploy in production!** This is an intentionally vulnerable environment.

### Testing:
```bash
# Run individual containers
docker-compose up mysql
docker-compose up vulnerable-web
docker-compose up ctf-platform

# View logs
docker-compose logs -f [service]
```

## 📊 Size Information

| Component | Approx Size |
|-----------|-------------|
| MySQL Image | ~500 MB |
| PHP-Apache Image | ~400 MB |
| Python Image | ~150 MB |
| Source Code | ~5 MB |
| **Total** | **~1 GB** |

## 🔧 Customization Points

### To modify challenges:
1. Edit `ctf-platform/app.py` - CHALLENGES list
2. Modify points, descriptions, hints

### To add new vulnerabilities:
1. Edit `vulnerable-web/app/pages/*.php`
2. Add new vulnerable endpoints
3. Update SQL schema if needed

### To change flag format:
1. Edit `flag-generator/generate_flags.py`
2. Modify `generate_flag()` function

### To add more challenges:
1. Add SQL flag injection in `generate_flags.py`
2. Add challenge definition in `app.py`
3. Update documentation

## 📝 Documentation Files

1. **README.md** - Main documentation (Vietnamese)
   - Overview
   - Installation
   - Usage
   - Challenges
   - Troubleshooting

2. **QUICKSTART.md** - 5-minute quick start
   - Prerequisites
   - 3 steps to run
   - Basic commands
   - Common issues

3. **PENTESTING_GUIDE.md** - Complete pentest guide
   - Methodology
   - Tools
   - AI integration
   - Sample solutions
   - Best practices

4. **PROJECT_STRUCTURE.md** - This file
   - File structure
   - Architecture
   - Component details

## 🎓 Educational Value

This project teaches:
- ✅ SQL Injection techniques
- ✅ Database security best practices (by showing bad practices)
- ✅ Pentesting methodology
- ✅ Docker containerization
- ✅ Web application security
- ✅ AI integration in security testing
- ✅ Professional reporting

## 🎉 Ready to Use

All files are created and ready. Just run:
```bash
cd database-security-ctf
setup.bat
```

And start hacking! 🚀
