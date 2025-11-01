#!/usr/bin/env python3
"""
Database Security CTF Platform
Main Flask Application
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
import json
import os
from datetime import datetime
import hashlib

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'de8cb8099eed36f0a1e555101380867aa68e51f335ebbaa2bd4e95d039a70286')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['ADMIN_PASSWORD'] = os.environ.get('CTF_ADMIN_PASSWORD', '1HZzDzR43Fq81_E7')

Session(app)

# Load flags from JSON file
def load_flags():
    try:
        with open('/app/flags.json', 'r') as f:
            data = json.load(f)
            return data['flags']
    except FileNotFoundError:
        # Fallback for development
        try:
            with open('flags.json', 'r') as f:
                data = json.load(f)
                return data['flags']
        except:
            return {}

# Challenge definitions - Redesigned for proper pentest workflow
# Total: 2000 points across 5 phases
CHALLENGES = [
    # ============================================================
    # PHASE 1: RECONNAISSANCE (200 points - 30 minutes)
    # ============================================================
    {
        'id': 1,
        'title': 'Network Scanning & Port Discovery',
        'category': 'Reconnaissance',
        'phase': 'Phase 1: Reconnaissance',
        'description': 'Perform network reconnaissance to identify open ports and services. Use nmap to scan the target and discover the MySQL service.',
        'points': 100,
        'estimated_time': '15 minutes',
        'difficulty': 'Easy',
        'learning_objectives': [
            'Use nmap for network scanning',
            'Understand service fingerprinting',
            'Identify open ports and running services'
        ],
        'hints': [
            'Start with basic nmap scan: nmap -sV -p- localhost',
            'Look for MySQL running on port 3306',
            'Connect to database and check system_info table for service_banner',
            'AI Tip: Ask ChatGPT to explain nmap flags and output'
        ],
        'tools': ['nmap', 'netcat', 'mysql client'],
        'ai_assistance': 'Use ChatGPT to explain nmap scan results and suggest next steps'
    },
    {
        'id': 2,
        'title': 'Database Version & Banner Grabbing',
        'category': 'Reconnaissance',
        'phase': 'Phase 1: Reconnaissance',
        'description': 'Extract MySQL version information and server details. Connect to the database and perform banner grabbing to gather system information.',
        'points': 100,
        'estimated_time': '15 minutes',
        'difficulty': 'Easy',
        'learning_objectives': [
            'Connect to MySQL server',
            'Extract version and configuration information',
            'Understand database fingerprinting techniques'
        ],
        'hints': [
            'Connect with: mysql -h localhost -P 3306 -u ctf_user -p (password in .env)',
            'Run: SELECT VERSION(); or SELECT @@version;',
            'Check system_info table: SELECT * FROM system_info WHERE info_key = "db_version";',
            'AI Tip: Use Claude to parse and analyze MySQL version output'
        ],
        'tools': ['mysql client', 'telnet'],
        'ai_assistance': 'Ask AI to identify known vulnerabilities for the MySQL version found'
    },

    # ============================================================
    # PHASE 2: MISCONFIGURATION DISCOVERY (400 points - 45 minutes)
    # ============================================================
    {
        'id': 3,
        'title': 'Weak Credentials Discovery',
        'category': 'Misconfiguration',
        'phase': 'Phase 2: Misconfiguration Discovery',
        'description': 'Identify users with weak or default credentials. Test common username/password combinations to find accounts with poor password security.',
        'points': 100,
        'estimated_time': '15 minutes',
        'difficulty': 'Easy',
        'learning_objectives': [
            'Understand the risk of default credentials',
            'Perform credential enumeration',
            'Use wordlist-based authentication testing'
        ],
        'hints': [
            'Look for backup or test users in mysql.user table',
            'Try common credentials: backup/backup123, test/test, admin/admin',
            'Login successful? Check users table for welcome_flag column',
            'AI Tip: Ask ChatGPT to generate a MySQL password wordlist'
        ],
        'tools': ['mysql client', 'hydra (optional)', 'custom Python script'],
        'ai_assistance': 'Generate common password wordlist with AI for MySQL users'
    },
    {
        'id': 4,
        'title': 'Excessive Privileges Detection',
        'category': 'Misconfiguration',
        'phase': 'Phase 2: Misconfiguration Discovery',
        'description': 'Audit user privileges and identify accounts with dangerous permissions like FILE, SUPER, or ALL PRIVILEGES.',
        'points': 150,
        'estimated_time': '15 minutes',
        'difficulty': 'Medium',
        'learning_objectives': [
            'Query mysql.user table for privilege information',
            'Understand MySQL privilege system',
            'Identify principle of least privilege violations'
        ],
        'hints': [
            'Query: SELECT User, Host, File_priv, Super_priv, Grant_priv FROM mysql.user;',
            'Look for users with File_priv = "Y" (can read files from system)',
            'Check user_privileges table for detailed grants',
            'AI Tip: Paste privilege output to AI and ask for security assessment'
        ],
        'tools': ['mysql client'],
        'ai_assistance': 'AI can analyze privilege dump and identify security risks'
    },
    {
        'id': 5,
        'title': 'Insecure Configuration Audit',
        'category': 'Misconfiguration',
        'phase': 'Phase 2: Misconfiguration Discovery',
        'description': 'Analyze MySQL server configuration for security weaknesses. Check variables like secure_file_priv, local_infile, and general_log.',
        'points': 150,
        'estimated_time': '15 minutes',
        'difficulty': 'Medium',
        'learning_objectives': [
            'Enumerate MySQL configuration variables',
            'Identify insecure settings',
            'Understand security implications of misconfigurations'
        ],
        'hints': [
            'Run: SHOW VARIABLES LIKE "%secure_file%";',
            'Run: SHOW VARIABLES LIKE "%local_infile%";',
            'Check config_audit table for flag',
            'AI Tip: Use AI to audit full configuration dump and explain risks'
        ],
        'tools': ['mysql client'],
        'ai_assistance': 'Export SHOW VARIABLES output and have AI perform security audit'
    },

    # ============================================================
    # PHASE 3: PRIVILEGE ESCALATION (450 points - 1 hour)
    # ============================================================
    {
        'id': 6,
        'title': 'Horizontal Privilege Escalation',
        'category': 'Privilege Escalation',
        'phase': 'Phase 3: Privilege Escalation',
        'description': 'Access data belonging to other users by exploiting weak access controls. Use SQL injection to view data you should not have access to.',
        'points': 200,
        'estimated_time': '30 minutes',
        'difficulty': 'Medium',
        'learning_objectives': [
            'Understand horizontal privilege escalation',
            'Exploit IDOR vulnerabilities',
            'Use UNION-based SQL injection to access other user data'
        ],
        'hints': [
            'Vulnerable endpoint: http://localhost:8080/index.php?page=profile&user_id=1',
            'Try changing user_id parameter to access other profiles',
            'Use UNION injection if filtering exists: user_id=1 UNION SELECT 1,2,private_data,4 FROM user_secrets--',
            'AI Tip: Generate UNION SELECT payloads with ChatGPT'
        ],
        'tools': ['Burp Suite', 'browser', 'sqlmap'],
        'ai_assistance': 'AI can generate SQL injection payloads for different column counts'
    },
    {
        'id': 7,
        'title': 'Vertical Privilege Escalation via Stored Procedures',
        'category': 'Privilege Escalation',
        'phase': 'Phase 3: Privilege Escalation',
        'description': 'Escalate from regular user to admin by exploiting stored procedures with elevated DEFINER privileges.',
        'points': 250,
        'estimated_time': '30 minutes',
        'difficulty': 'Hard',
        'learning_objectives': [
            'Enumerate stored procedures and functions',
            'Understand SQL DEFINER security model',
            'Exploit procedures running with elevated privileges'
        ],
        'hints': [
            'List procedures: SHOW PROCEDURE STATUS WHERE Db = "ctf_database";',
            'Check procedure definition: SHOW CREATE PROCEDURE get_admin_flag;',
            'Notice DEFINER=root - this runs with root privileges!',
            'Execute: CALL get_admin_flag(); to get the flag',
            'AI Tip: Ask AI to explain DEFINER security implications'
        ],
        'tools': ['mysql client'],
        'ai_assistance': 'AI can explain stored procedure security model and identify risks'
    },

    # ============================================================
    # PHASE 4: INJECTION ATTACKS (500 points - 1.5 hours)
    # ============================================================
    {
        'id': 8,
        'title': 'Authentication Bypass via SQL Injection',
        'category': 'Injection',
        'phase': 'Phase 4: Injection Attacks',
        'description': 'Bypass the login form using classic SQL injection techniques. Access the admin panel without knowing the password.',
        'points': 200,
        'estimated_time': '30 minutes',
        'difficulty': 'Medium',
        'learning_objectives': [
            'Understand SQL injection in authentication',
            'Craft payloads to bypass login logic',
            'Exploit lack of input validation'
        ],
        'hints': [
            'Target: http://localhost:8080/index.php?page=login',
            'Try username: admin\' OR \'1\'=\'1\' -- and any password',
            'Alternative: admin\' #',
            'After successful login, navigate to admin panel for flag',
            'AI Tip: Ask ChatGPT to generate various SQLi authentication bypass payloads'
        ],
        'tools': ['Burp Suite', 'browser', 'curl'],
        'ai_assistance': 'Generate multiple SQLi bypass payloads with AI for different DB types'
    },
    {
        'id': 9,
        'title': 'Blind SQL Injection & Data Exfiltration',
        'category': 'Injection',
        'phase': 'Phase 4: Injection Attacks',
        'description': 'Extract sensitive data using blind SQL injection techniques. Automate the exploitation with custom scripts or AI assistance.',
        'points': 300,
        'estimated_time': '1 hour',
        'difficulty': 'Hard',
        'learning_objectives': [
            'Understand boolean-based and time-based blind SQLi',
            'Automate data extraction with scripts',
            'Use AI to optimize exploitation speed'
        ],
        'hints': [
            'Target: http://localhost:8080/index.php?page=product_detail&id=1',
            'Test: id=1 AND 1=1 (true) vs id=1 AND 1=2 (false)',
            'Extract flag character by character: id=1 AND SUBSTRING((SELECT hidden_flag FROM products LIMIT 1),1,1)="F"',
            'Use sqlmap: sqlmap -u "http://localhost:8080/index.php?page=product_detail&id=1" --dump',
            'AI Tip: Use ai-helpers/blind_sqli_ai.py to optimize character guessing'
        ],
        'tools': ['sqlmap', 'Python script', 'Burp Suite Intruder'],
        'ai_assistance': 'AI can optimize blind SQLi by suggesting next character based on frequency analysis'
    },

    # ============================================================
    # PHASE 5: KEY EXTRACTION (250 points - 45 minutes)
    # ============================================================
    {
        'id': 10,
        'title': 'Master Key Extraction via Multi-Stage Attack',
        'category': 'Key Extraction',
        'phase': 'Phase 5: Key Extraction',
        'description': 'Combine all learned techniques to extract the master key. The flag is split across multiple locations: file system, logs, and triggers.',
        'points': 250,
        'estimated_time': '45 minutes',
        'difficulty': 'Expert',
        'learning_objectives': [
            'Combine multiple exploitation techniques',
            'Use LOAD_FILE() to read system files',
            'Analyze audit logs and database triggers',
            'Synthesize information from multiple sources'
        ],
        'hints': [
            'Part 1: Use LOAD_FILE() to read /var/lib/mysql/secret_part1.txt (requires FILE privilege from Challenge 4)',
            'Part 2: Analyze audit_log table for encoded flag parts',
            'Part 3: Extract from trigger definition: SHOW CREATE TRIGGER master_key_trigger;',
            'Combine all parts to form final flag: FLAG{part1_part2_part3}',
            'AI Tip: Use ai-helpers/log_analyzer.py to correlate log entries'
        ],
        'tools': ['mysql client', 'Python script', 'text editor'],
        'ai_assistance': 'AI can help correlate data from multiple sources and reconstruct the master key'
    }
]

@app.route('/')
def index():
    """Main dashboard showing all challenges"""
    # Initialize session data
    if 'solved_challenges' not in session:
        session['solved_challenges'] = []

    if 'score' not in session:
        session['score'] = 0

    if 'username' not in session:
        session['username'] = 'Anonymous'

    # Calculate total possible points
    total_points = sum(c['points'] for c in CHALLENGES)

    return render_template('index.html',
                         challenges=CHALLENGES,
                         solved=session['solved_challenges'],
                         score=session['score'],
                         total_points=total_points,
                         username=session['username'])

@app.route('/challenge/<int:challenge_id>')
def challenge(challenge_id):
    """Individual challenge page"""
    challenge = next((c for c in CHALLENGES if c['id'] == challenge_id), None)

    if not challenge:
        return "Challenge not found", 404

    is_solved = challenge_id in session.get('solved_challenges', [])

    return render_template('challenge.html',
                         challenge=challenge,
                         is_solved=is_solved)

@app.route('/submit', methods=['POST'])
def submit_flag():
    """Submit a flag for verification"""
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    submitted_flag = data.get('flag', '').strip()

    # Load correct flags
    flags = load_flags()

    # Get challenge
    challenge = next((c for c in CHALLENGES if c['id'] == challenge_id), None)

    if not challenge:
        return jsonify({'success': False, 'message': 'Invalid challenge ID'})

    # Check if already solved
    if challenge_id in session.get('solved_challenges', []):
        return jsonify({'success': False, 'message': 'You already solved this challenge!'})

    # Get correct flag
    correct_flag = flags.get(str(challenge_id), {}).get('flag', '')

    if not correct_flag:
        return jsonify({'success': False, 'message': 'Flag not available. Please run generate_flags.py'})

    # Verify flag
    if submitted_flag == correct_flag:
        # Mark as solved
        if 'solved_challenges' not in session:
            session['solved_challenges'] = []

        session['solved_challenges'].append(challenge_id)
        session['score'] = session.get('score', 0) + challenge['points']
        session.modified = True

        return jsonify({
            'success': True,
            'message': f'Correct! +{challenge["points"]} points',
            'score': session['score']
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Incorrect flag. Try again!'
        })

@app.route('/hints/<int:challenge_id>')
def get_hints(challenge_id):
    """Get hints for a challenge"""
    challenge = next((c for c in CHALLENGES if c['id'] == challenge_id), None)

    if not challenge:
        return jsonify({'success': False, 'message': 'Challenge not found'})

    return jsonify({
        'success': True,
        'hints': challenge['hints']
    })

@app.route('/scoreboard')
def scoreboard():
    """Show current score and progress"""
    total_points = sum(c['points'] for c in CHALLENGES)
    solved_count = len(session.get('solved_challenges', []))
    current_score = session.get('score', 0)

    progress = (current_score / total_points * 100) if total_points > 0 else 0

    return render_template('scoreboard.html',
                         score=current_score,
                         total_points=total_points,
                         solved_count=solved_count,
                         total_challenges=len(CHALLENGES),
                         progress=progress,
                         challenges=CHALLENGES,
                         solved=session.get('solved_challenges', []))

@app.route('/reset', methods=['POST'])
def reset():
    """Reset progress (for testing)"""
    session.clear()
    session['username'] = 'Anonymous'
    session['solved_challenges'] = []
    session['score'] = 0
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login for tracking"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/about')
def about():
    """About page with instructions"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
