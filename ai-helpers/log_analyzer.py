#!/usr/bin/env python3
"""
AI-Powered Log Correlation and Analysis Tool
For Challenge 10: Master Key Extraction via Multi-Stage Attack

Correlates data from multiple sources to reconstruct the master key.
"""

import argparse
import pymysql
import re
import sys


class LogAnalyzer:
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

    def analyze_audit_logs(self):
        """Analyze audit_log table for key fragments"""
        print("\n[*] Analyzing audit logs...")
        print("=" * 70)

        self.cursor.execute("SELECT * FROM audit_log;")
        logs = self.cursor.fetchall()

        fragments = {}

        for log in logs:
            log_id, action, flag, user_agent, timestamp = log
            print(f"[{log_id}] {timestamp} | {action}")

            # Look for key fragments
            if 'KEY_PART' in str(flag):
                match = re.search(r'KEY_PART_(\d+):\s*(\S+)', str(flag))
                if match:
                    part_num = match.group(1)
                    part_value = match.group(2)
                    fragments[f'part{part_num}'] = part_value
                    print(f"    -> Found KEY_PART_{part_num}: {part_value}")

            if 'reconstruction_hint' in action.lower():
                print(f"    -> Hint: {flag}")

        print()
        return fragments

    def read_file_references(self):
        """Read file_references table for file-based key parts"""
        print("[*] Checking file references...")
        print("=" * 70)

        self.cursor.execute("SELECT * FROM file_references WHERE file_type = 'secret';")
        files = self.cursor.fetchall()

        fragments = {}

        for file_ref in files:
            file_id, filename, content, file_type, timestamp = file_ref
            print(f"[{file_id}] {filename}")

            # Extract key part from content
            match = re.search(r'KEY_PART_(\d+):\s*(\S+)', str(content))
            if match:
                part_num = match.group(1)
                part_value = match.group(2)
                fragments[f'part{part_num}'] = part_value
                print(f"    -> Found KEY_PART_{part_num}: {part_value}")
                print(f"    -> Location: {filename}")
                print(f"    -> Use: SELECT LOAD_FILE('{filename}'); to verify")

        print()
        return fragments

    def check_triggers(self):
        """Check trigger definitions for embedded keys"""
        print("[*] Analyzing database triggers...")
        print("=" * 70)

        self.cursor.execute("SHOW TRIGGERS;")
        triggers = self.cursor.fetchall()

        fragments = {}

        for trigger in triggers:
            trigger_name = trigger[0]
            print(f"[*] Trigger: {trigger_name}")

            # Get trigger definition
            self.cursor.execute(f"SHOW CREATE TRIGGER {trigger_name};")
            definition = self.cursor.fetchone()

            if definition:
                trigger_sql = definition[2]  # SQL statement

                # Look for key parts in comments
                match = re.search(r'Master Key Part (\d+):\s*(\S+)', trigger_sql)
                if match:
                    part_num = match.group(1)
                    part_value = match.group(2)
                    fragments[f'part{part_num}'] = part_value
                    print(f"    -> Found KEY_PART_{part_num}: {part_value}")
                    print(f"    -> Location: Trigger definition comment")

        print()
        return fragments

    def reconstruct_master_key(self, all_fragments):
        """Reconstruct master key from all fragments"""
        print("=" * 70)
        print("[*] RECONSTRUCTING MASTER KEY")
        print("=" * 70)
        print()

        print("[*] Collected Fragments:")
        for key, value in sorted(all_fragments.items()):
            print(f"    {key}: {value}")
        print()

        # Combine parts in order
        if 'part1' in all_fragments and 'part2' in all_fragments and 'part3' in all_fragments:
            master_key = all_fragments['part1'] + all_fragments['part2'] + all_fragments['part3']
            final_flag = f"FLAG{{{master_key}}}"

            print("[SUCCESS] Master Key Reconstructed!")
            print("=" * 70)
            print(f"Part 1: {all_fragments['part1']}")
            print(f"Part 2: {all_fragments['part2']}")
            print(f"Part 3: {all_fragments['part3']}")
            print()
            print(f"MASTER KEY: {final_flag}")
            print("=" * 70)

            return final_flag
        else:
            missing = []
            for i in range(1, 4):
                if f'part{i}' not in all_fragments:
                    missing.append(f'part{i}')

            print("[!] Incomplete key fragments!")
            print(f"[!] Missing: {', '.join(missing)}")
            print()
            print("Hints:")
            if 'part1' not in all_fragments:
                print("  - Part 1: Check file_references table and use LOAD_FILE()")
            if 'part2' not in all_fragments:
                print("  - Part 2: Check audit_log table for 'master_key_fragment'")
            if 'part3' not in all_fragments:
                print("  - Part 3: Check trigger definitions with SHOW CREATE TRIGGER")

            return None

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Log Correlation and Analysis Tool",
        epilog="Example: python log_analyzer.py --host localhost --user ctf_user --password <from .env>"
    )

    parser.add_argument('--host', default='localhost', help='MySQL host (default: localhost)')
    parser.add_argument('--port', type=int, default=3306, help='MySQL port (default: 3306)')
    parser.add_argument('--user', required=True, help='MySQL username')
    parser.add_argument('--password', required=True, help='MySQL password')
    parser.add_argument('--database', default='ctf_database', help='Database name (default: ctf_database)')

    args = parser.parse_args()

    print("=" * 70)
    print("AI-Powered Log Correlation and Analysis Tool")
    print("For Challenge 10: Master Key Extraction")
    print("=" * 70)

    analyzer = LogAnalyzer(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )

    try:
        # Collect fragments from all sources
        all_fragments = {}

        # Source 1: Audit logs
        log_fragments = analyzer.analyze_audit_logs()
        all_fragments.update(log_fragments)

        # Source 2: File references
        file_fragments = analyzer.read_file_references()
        all_fragments.update(file_fragments)

        # Source 3: Triggers
        trigger_fragments = analyzer.check_triggers()
        all_fragments.update(trigger_fragments)

        # Reconstruct master key
        master_key = analyzer.reconstruct_master_key(all_fragments)

        if master_key:
            print()
            print("Next steps:")
            print("1. Submit the master key to the CTF platform")
            print("2. Congratulations on completing all 10 challenges!")
            print("3. Write a comprehensive pentest report documenting your findings")
        else:
            print()
            print("[*] Continue investigating to find all key fragments")

    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
