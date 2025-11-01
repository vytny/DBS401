#!/usr/bin/env python3
"""
AI-Powered MySQL Configuration Security Auditor
For Challenge 5: Insecure Configuration Audit

Automatically audits MySQL configuration for security issues
using AI to explain risks and suggest mitigations.
"""

import argparse
import pymysql
import sys
import json


class MySQLConfigAuditor:
    def __init__(self, host, port, user, password, database='ctf_database'):
        """Initialize MySQL connection"""
        try:
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print(f"[+] Connected to MySQL: {user}@{host}:{port}/{database}")
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            sys.exit(1)

    def get_all_variables(self):
        """Get all MySQL system variables"""
        self.cursor.execute("SHOW VARIABLES;")
        variables = {}
        for row in self.cursor.fetchall():
            variables[row[0]] = row[1]
        return variables

    def audit_security_variables(self):
        """Audit security-critical variables"""
        print("\n" + "=" * 70)
        print("MySQL SECURITY CONFIGURATION AUDIT")
        print("=" * 70)
        print()

        critical_vars = {
            'secure_file_priv': {
                'secure_value': '/var/lib/mysql-files/',
                'risk': 'CRITICAL',
                'description': 'Controls file read/write locations'
            },
            'local_infile': {
                'secure_value': 'OFF',
                'risk': 'HIGH',
                'description': 'Allows loading local files'
            },
            'skip_name_resolve': {
                'secure_value': 'ON',
                'risk': 'MEDIUM',
                'description': 'DNS resolution for connections'
            },
            'validate_password.policy': {
                'secure_value': 'STRONG',
                'risk': 'HIGH',
                'description': 'Password complexity requirements'
            },
            'log_bin': {
                'secure_value': 'ON',
                'risk': 'MEDIUM',
                'description': 'Binary logging for replication/recovery'
            }
        }

        all_vars = self.get_all_variables()
        findings = []

        for var_name, var_info in critical_vars.items():
            current_value = all_vars.get(var_name, 'NOT SET')
            secure_value = var_info['secure_value']
            risk = var_info['risk']

            is_secure = current_value == secure_value
            status = "[SECURE]" if is_secure else f"[{risk} RISK]"

            finding = {
                'variable': var_name,
                'current_value': current_value,
                'secure_value': secure_value,
                'risk_level': risk,
                'is_secure': is_secure,
                'description': var_info['description']
            }

            findings.append(finding)

            # Print finding
            print(f"{status} {var_name}")
            print(f"    Current: {current_value}")
            print(f"    Secure:  {secure_value}")
            print(f"    Impact:  {var_info['description']}")

            if not is_secure:
                print(f"    AI Analysis: {self.ai_explain_risk(var_name, current_value)}")
            print()

        return findings

    def ai_explain_risk(self, variable, value):
        """
        AI-powered risk explanation
        (Placeholder - in production would call OpenAI/Claude API)
        """
        explanations = {
            'secure_file_priv': "Empty value allows reading ANY file on filesystem using LOAD_FILE(). Attackers can read /etc/passwd, SSH keys, application secrets.",
            'local_infile': "ON allows LOAD DATA LOCAL INFILE which can leak sensitive files from client machines to the server.",
            'skip_name_resolve': "OFF causes DNS lookups which can be slow and vulnerable to DNS poisoning attacks.",
            'validate_password.policy': "Weak policy allows simple passwords like '123456', making brute-force attacks trivial.",
            'log_bin': "OFF disables binary logging, making point-in-time recovery impossible after attacks."
        }

        return explanations.get(variable, "Configuration may allow security vulnerabilities.")

    def check_for_flag(self):
        """Check config_audit table for flag"""
        try:
            self.cursor.execute("SELECT * FROM config_audit WHERE risk_level = 'CRITICAL';")
            results = self.cursor.fetchall()

            if results:
                print("=" * 70)
                print("[FLAG FOUND IN CONFIG_AUDIT TABLE]")
                print("=" * 70)
                for row in results:
                    print(f"Config: {row[1]} = {row[2]}")
                    print(f"Risk: {row[3]}")
                    print(f"Flag: {row[4]}")
                print()
                return row[4]
        except Exception as e:
            print(f"[*] Note: config_audit table not found or inaccessible: {e}")

        return None

    def generate_report(self, findings, output_file=None):
        """Generate audit report"""
        report = {
            'summary': {
                'total_checks': len(findings),
                'secure': sum(1 for f in findings if f['is_secure']),
                'insecure': sum(1 for f in findings if not f['is_secure']),
                'critical_risks': sum(1 for f in findings if not f['is_secure'] and f['risk_level'] == 'CRITICAL')
            },
            'findings': findings
        }

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"[+] Report saved to {output_file}")

        return report

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered MySQL Configuration Security Auditor",
        epilog="Example: python config_auditor.py --host localhost --user ctf_user --password <from .env>"
    )

    parser.add_argument('--host', default='localhost', help='MySQL host (default: localhost)')
    parser.add_argument('--port', type=int, default=3306, help='MySQL port (default: 3306)')
    parser.add_argument('--user', required=True, help='MySQL username')
    parser.add_argument('--password', required=True, help='MySQL password')
    parser.add_argument('--database', default='ctf_database', help='Database name (default: ctf_database)')
    parser.add_argument('--report', help='Save report to JSON file')

    args = parser.parse_args()

    print("=" * 70)
    print("AI-Powered MySQL Configuration Security Auditor")
    print("For Challenge 5: Insecure Configuration Audit")
    print("=" * 70)

    auditor = MySQLConfigAuditor(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )

    try:
        # Perform audit
        findings = auditor.audit_security_variables()

        # Check for flag
        flag = auditor.check_for_flag()

        # Generate report
        report = auditor.generate_report(findings, output_file=args.report)

        # Summary
        print("=" * 70)
        print("AUDIT SUMMARY")
        print("=" * 70)
        print(f"Total Checks: {report['summary']['total_checks']}")
        print(f"Secure: {report['summary']['secure']}")
        print(f"Insecure: {report['summary']['insecure']}")
        print(f"Critical Risks: {report['summary']['critical_risks']}")
        print()

        if flag:
            print(f"[SUCCESS] Flag found: {flag}")
            print()
            print("Next steps:")
            print("1. Submit the flag to the CTF platform")
            print("2. Review the security findings above")
            print("3. Research how to fix each misconfiguration")
        else:
            print("[*] No flag found in config_audit table")
            print("[*] Try querying: SELECT * FROM config_audit;")

    finally:
        auditor.close()


if __name__ == "__main__":
    main()
