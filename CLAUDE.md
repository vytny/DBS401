# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **educational CTF (Capture The Flag) platform** for learning database security and penetration testing designed for **4th-year university students** with a **half-day to full-day lab duration** (4-5 hours).

**REDESIGN STATUS (2025-10-20):** ✅ 75% Complete - Core features implemented
- See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for full status
- See [REDESIGN_PLAN.md](REDESIGN_PLAN.md) for architecture details
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing instructions

**CRITICAL**: This project contains deliberate security vulnerabilities. Never deploy to production or expose to public networks. All vulnerabilities are educational.

## Architecture

The project uses Docker Compose to orchestrate three containers:

1. **MySQL Database** (`mysql/`) - Intentionally vulnerable database with weak configuration
2. **Vulnerable Web App** (`vulnerable-web/`) - PHP application with SQL injection vulnerabilities
3. **CTF Platform** (`ctf-platform/`) - Flask application for challenge management and flag validation

### Data Flow

```
Flag Generator (Python) → Generates unique flags per instance
    ↓
    • Creates flags.json (flag validation data)
    • Creates .env (passwords & secrets)
    • Creates mysql/init/02-flags.sql (database flag injection)
    ↓
Docker Compose builds and starts all services
    ↓
Users attack vulnerable-web (port 8080) and mysql (port 3306)
    ↓
Users submit found flags to ctf-platform (port 5000) for validation
```

## Development Commands

### Initial Setup

```bash
# Windows
setup.bat

# Manual setup
cd flag-generator
python generate_flags.py
cd ..
docker-compose up -d
```

### Container Management

```bash
# View logs
docker-compose logs -f
docker-compose logs mysql
docker-compose logs vulnerable-web
docker-compose logs ctf-platform

# Stop/restart
docker-compose down
docker-compose restart

# Rebuild after code changes
docker-compose down
docker-compose build
docker-compose up -d

# Check status
docker-compose ps

# Access MySQL shell
docker exec -it ctf-mysql mysql -u root -p
# Password from .env file MYSQL_ROOT_PASSWORD
```

### Flag Generation

```bash
# Regenerate all flags (creates new .env and flags)
cd flag-generator
python generate_flags.py

# Generated files:
#   - ../flags.json (flag definitions for CTF platform)
#   - ../.env (environment variables with passwords)
#   - ../mysql/init/02-flags.sql (SQL statements to inject flags)
```

### Reset Environment

```bash
# Complete reset with new flags
docker-compose down -v
python flag-generator/generate_flags.py
docker-compose up -d
```

## Important File Locations

### Auto-Generated Files (Never Commit)
- `.env` - Contains all passwords and secrets
- `flags.json` - Flag validation data used by CTF platform
- `mysql/init/02-flags.sql` - SQL statements to inject flags into database

### Core Application Files
- `ctf-platform/app.py` - Main Flask app with CHALLENGES array (39-160)
- `flag-generator/generate_flags.py` - Flag generation logic
- `mysql/init/01-schema.sql` - Database schema (runs before 02-flags.sql)
- `vulnerable-web/app/db.php` - Intentionally vulnerable database functions

## Redesigned Pentest Workflow (NEW - Oct 2025)

The 10 challenges now follow proper penetration testing methodology:

**Phase 1: RECONNAISSANCE** (200 pts, 30 min)
- Challenge 1: Network Scanning & Port Discovery
- Challenge 2: Database Version & Banner Grabbing

**Phase 2: MISCONFIGURATION DISCOVERY** (400 pts, 45 min)
- Challenge 3: Weak Credentials Discovery
- Challenge 4: Excessive Privileges Detection
- Challenge 5: Insecure Configuration Audit

**Phase 3: PRIVILEGE ESCALATION** (450 pts, 1 hour)
- Challenge 6: Horizontal Privilege Escalation
- Challenge 7: Vertical Privilege Escalation via Stored Procedures

**Phase 4: INJECTION ATTACKS** (500 pts, 1.5 hours)
- Challenge 8: Authentication Bypass via SQL Injection
- Challenge 9: Blind SQL Injection & Data Exfiltration

**Phase 5: KEY EXTRACTION** (250 pts, 45 min)
- Challenge 10: Master Key Extraction via Multi-Stage Attack

**Total:** 2000 points, ~4.5 hours

## Challenge System

Challenges are defined in `ctf-platform/app.py` in the `CHALLENGES` array (lines 40-295). Each challenge now has:
- `id` - Numeric identifier (1-10)
- `title` - Challenge name
- `category` - Reconnaissance, Misconfiguration, Privilege Escalation, Injection, Key Extraction
- `phase` - Which phase it belongs to (NEW)
- `description` - What the user needs to do
- `points` - Score value
- `estimated_time` - How long it should take (NEW)
- `difficulty` - Easy/Medium/Hard/Expert (NEW)
- `learning_objectives` - Educational goals (NEW)
- `tools` - Recommended tools (NEW)
- `ai_assistance` - How AI can help (NEW)
- `hints` - Array of progressive hints

Flags are now injected into different database locations:
1. Challenge 1: `system_info.service_banner`
2. Challenge 2: `system_info.db_version`
3. Challenge 3: `users.welcome_flag` (after weak cred login)
4. Challenge 4: `user_privileges.discovery_flag`
5. Challenge 5: `config_audit.audit_flag`
6. Challenge 6: `user_secrets.secret_key`
7. Challenge 7: Stored procedure `get_admin_flag()` output
8. Challenge 8: `admin_panel.secret_key`
9. Challenge 9: `products.hidden_flag`
10. Challenge 10: Split across 3 locations (file, audit_log, trigger) - must combine

## Modifying Challenges

### To Change Challenge Descriptions/Points

Edit `ctf-platform/app.py` CHALLENGES array, then rebuild:
```bash
docker-compose restart ctf-platform
```

### To Add New Challenges

1. Edit `flag-generator/generate_flags.py`:
   - Add challenge to `generate_all_flags()` method
   - Add SQL injection logic in `generate_sql_init()` method

2. Edit `ctf-platform/app.py`:
   - Add challenge definition to CHALLENGES array

3. Edit `mysql/init/01-schema.sql` if new tables needed

4. Regenerate and rebuild:
```bash
python flag-generator/generate_flags.py
docker-compose down -v
docker-compose up -d
```

## Vulnerable Code Patterns

The vulnerable web application intentionally contains:

- **SQL Injection**: String concatenation in `vulnerable-web/app/db.php` (lines 42-50)
  - `getUserByCredentials()` - Direct concatenation of username/password
  - All pages use `executeQuery()` which doesn't sanitize input

- **Debug Mode**: Enabled in config, exposes SQL queries in HTML comments

- **Information Disclosure**: Error messages reveal SQL structure

These vulnerabilities are **educational by design** - do not "fix" them unless specifically requested.

## Database Configuration

MySQL is configured with weak security in `mysql/my.cnf`:
- `secure_file_priv=""` - Allows reading any file
- Local infile enabled
- General log enabled for debugging

These settings enable challenges 5, 7, and 10 (Config Audit, Privilege Escalation, Log Analysis).

## AI Integration (NEW - Oct 2025)

The `ai-helpers/` directory contains 4 Python scripts demonstrating AI-augmented pentesting:

### 1. wordlist_generator.py (Challenge 3)
Generates MySQL-specific password wordlists using OpenAI API.
```bash
cd ai-helpers
python wordlist_generator.py --api-key YOUR_KEY --output mysql_pass.txt
# Or without AI:
python wordlist_generator.py --fallback
```

### 2. blind_sqli_optimizer.py (Challenge 9)
Optimizes blind SQL injection using frequency analysis.
```bash
python blind_sqli_optimizer.py --target http://localhost:8080/index.php?page=product_detail --param id
```

### 3. config_auditor.py (Challenge 5)
AI-powered MySQL configuration security audit.
```bash
python config_auditor.py --user ctf_user --password <from .env>
```

### 4. log_analyzer.py (Challenge 10)
Correlates logs and reconstructs the master key.
```bash
python log_analyzer.py --user ctf_user --password <from .env>
```

**Dependencies:** `pip install -r ai-helpers/requirements.txt`

**Note:** All AI tools have fallback modes and work without API keys (with reduced functionality).

## Port Mapping

- Port 5000: CTF Platform (Flask)
- Port 8080: Vulnerable Web App (PHP/Apache)
- Port 3306: MySQL Database

All ports bound to localhost only for safety.

## Environment Variables

All loaded from `.env` file (auto-generated):
- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `MYSQL_DATABASE` - Always "ctf_database"
- `MYSQL_USER` - Always "ctf_user"
- `MYSQL_PASSWORD` - MySQL user password
- `CTF_SECRET_KEY` - Flask secret key
- `CTF_ADMIN_PASSWORD` - CTF platform admin password
- `WEB_SESSION_SECRET` - Web app session secret
- `INSTANCE_SALT` - Used to generate unique flags

## Testing Workflow

1. Start environment: `setup.bat` or `docker-compose up -d`
2. Access CTF platform: http://localhost:5000
3. View challenges and hints
4. Attack targets:
   - Vulnerable web: http://localhost:8080
   - MySQL: `mysql -h localhost -P 3306 -u ctf_user -p`
5. Submit flags on CTF platform
6. Check logs: `docker-compose logs -f`

## Educational Purpose

This is a **defensive security educational tool**. When working with this code:
- Analyze vulnerabilities to understand how they work
- Explain security issues and their impacts
- Help create documentation or detection rules
- Assist with understanding the pentesting workflow

Do NOT:
- Create additional malicious code
- Help deploy this to production
- Assist with actual credential harvesting
- Modify code to make vulnerabilities harder to detect

## Documentation

- [README.md](README.md) - Full project documentation (Vietnamese)
- [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed file structure
- [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md) - Penetration testing methodology
