# AI Integration Tools for Database Security CTF

This directory contains AI-powered helper scripts to assist with pentesting challenges.

## Overview

These tools demonstrate how AI can augment traditional penetration testing workflows, making the process more efficient and educational.

## Available Tools

### 1. `wordlist_generator.py`
Generate custom MySQL password wordlists using AI (ChatGPT/Claude).

**Usage:**
```bash
python wordlist_generator.py --api-key YOUR_API_KEY --output mysql_passwords.txt
```

**Challenge:** 3 - Weak Credentials Discovery

---

### 2. `blind_sqli_optimizer.py`
Optimize blind SQL injection attacks using AI to predict next characters based on frequency analysis.

**Usage:**
```bash
python blind_sqli_optimizer.py --target http://localhost:8080/index.php?page=product_detail --param id
```

**Challenge:** 9 - Blind SQL Injection

---

### 3. `config_auditor.py`
Automated MySQL configuration security audit powered by AI.

**Usage:**
```bash
python config_auditor.py --host localhost --user ctf_user --password <from .env>
```

**Challenge:** 5 - Insecure Configuration Audit

---

### 4. `log_analyzer.py`
AI-powered log correlation and analysis for multi-stage attacks.

**Usage:**
```bash
python log_analyzer.py --logs audit_log_dump.txt
```

**Challenge:** 10 - Master Key Extraction

---

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Keys

Create a `.env` file in this directory:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note:** AI tools are optional. Challenges can be solved without them, but AI assistance significantly speeds up the process and provides learning insights.

---

## How AI Helps in Pentesting

### 1. **Pattern Recognition**
AI can analyze error messages, response patterns, and identify vulnerabilities faster than manual analysis.

### 2. **Payload Generation**
Generate context-aware SQL injection payloads, XSS vectors, and other attack strings.

### 3. **Data Correlation**
Correlate information from multiple sources (logs, databases, files) to piece together complex attacks.

### 4. **Learning Assistant**
AI explains vulnerabilities, suggests mitigation strategies, and provides educational context.

---

## Educational Goals

Students learn to:
- ✅ Integrate AI APIs into security tools
- ✅ Understand when AI helps vs. when manual analysis is needed
- ✅ Develop custom automation scripts
- ✅ Combine traditional pentesting with modern AI capabilities

---

## Ethical Usage

These tools are for educational purposes in controlled environments only:
- ✅ Use in CTF lab environments
- ✅ Use for authorized pentests
- ✅ Use for security research

- ❌ DO NOT use on unauthorized systems
- ❌ DO NOT use for malicious purposes
- ❌ DO NOT violate computer fraud laws

---

## Alternative Approaches

If you don't have AI API access:
1. Use free AI chat interfaces (ChatGPT web, Claude.ai)
2. Copy-paste outputs into AI for analysis
3. Use traditional tools (sqlmap, hydra, etc.)
4. Manual analysis is still the best learning method!

---

## Support

For questions or issues:
1. Read tool help: `python <tool>.py --help`
2. Check example outputs in `examples/` folder
3. Review challenge hints in CTF platform
4. Ask instructor for guidance
