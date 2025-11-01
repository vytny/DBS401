#!/usr/bin/env python3
"""
Flag Generator for Database Security CTF
Generates unique flags for each Docker instance using a random salt
"""

import hashlib
import secrets
import json
import os
import sys

class FlagGenerator:
    def __init__(self, instance_salt=None):
        """
        Initialize flag generator with instance salt
        If no salt provided, generate a new one
        """
        self.instance_salt = instance_salt or secrets.token_hex(16)
        self.flags = {}

    def generate_flag(self, challenge_id, challenge_name):
        """
        Generate a unique flag for a specific challenge
        Format: FLAG{hash_based_on_challenge_and_salt}
        """
        secret = f"{challenge_id}_{challenge_name}_{self.instance_salt}".encode()
        flag_hash = hashlib.sha256(secret).hexdigest()[:20]
        flag = f"FLAG{{{flag_hash}}}"

        self.flags[challenge_id] = {
            "name": challenge_name,
            "flag": flag,
            "id": challenge_id
        }

        return flag

    def generate_all_flags(self):
        """Generate flags for all 10 challenges - Redesigned pentest workflow"""

        challenges = [
            # Phase 1: Reconnaissance
            (1, "network_scanning", "Network Scanning & Port Discovery"),
            (2, "banner_grabbing", "Database Version & Banner Grabbing"),

            # Phase 2: Misconfiguration Discovery
            (3, "weak_credentials", "Weak Credentials Discovery"),
            (4, "excessive_privileges", "Excessive Privileges Detection"),
            (5, "insecure_config", "Insecure Configuration Audit"),

            # Phase 3: Privilege Escalation
            (6, "horizontal_privesc", "Horizontal Privilege Escalation"),
            (7, "vertical_privesc", "Vertical Privilege Escalation via Stored Procedures"),

            # Phase 4: Injection Attacks
            (8, "auth_bypass_sqli", "Authentication Bypass via SQL Injection"),
            (9, "blind_sqli", "Blind SQL Injection & Data Exfiltration"),

            # Phase 5: Key Extraction
            (10, "master_key", "Master Key Extraction via Multi-Stage Attack")
        ]

        print("=" * 70)
        print("PENTEST WORKFLOW - FLAG GENERATION")
        print("=" * 70)
        print()

        for challenge_id, challenge_key, challenge_name in challenges:
            flag = self.generate_flag(challenge_id, challenge_key)

            # Print with phase indicators
            if challenge_id in [1, 2]:
                phase = "PHASE 1: RECONNAISSANCE"
            elif challenge_id in [3, 4, 5]:
                phase = "PHASE 2: MISCONFIGURATION"
            elif challenge_id in [6, 7]:
                phase = "PHASE 3: PRIVILEGE ESCALATION"
            elif challenge_id in [8, 9]:
                phase = "PHASE 4: INJECTION"
            else:
                phase = "PHASE 5: KEY EXTRACTION"

            if challenge_id in [1, 3, 6, 8, 10]:
                print(f"\n{phase}")
                print("-" * 70)

            print(f"[{challenge_id:02d}] {challenge_name}")
            print(f"     Flag: {flag}")

        print()
        print("=" * 70)
        return self.flags

    def save_to_json(self, output_file="flags.json"):
        """Save generated flags to JSON file"""
        output_data = {
            "instance_salt": self.instance_salt,
            "flags": self.flags
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)

        print(f"[OK] Flags saved to {output_file}")

    def generate_sql_init(self, output_file="flags_init.sql"):
        """Generate SQL statements to inject flags into database - Redesigned"""

        sql_statements = [
            "-- ============================================================",
            "-- Auto-generated SQL for Flag Injection",
            "-- Database Security CTF - Pentest Workflow Design",
            "-- ============================================================",
            "-- Generated with unique instance salt for this deployment",
            "-- DO NOT MANUALLY EDIT THIS FILE",
            "-- ============================================================\n",
            "USE ctf_database;\n"
        ]

        # ============================================================
        # PHASE 1: RECONNAISSANCE
        # ============================================================
        sql_statements.append("-- ============================================================")
        sql_statements.append("-- PHASE 1: RECONNAISSANCE")
        sql_statements.append("-- ============================================================\n")

        # Challenge 1: Network Scanning & Port Discovery
        flag1 = self.flags[1]["flag"]
        sql_statements.append(f"-- Challenge 1: Network Scanning & Port Discovery")
        sql_statements.append(f"-- Flag location: system_info table -> service_banner column")
        sql_statements.append(f"INSERT INTO system_info (info_key, info_value) VALUES ('service_banner', '{flag1}');\n")

        # Challenge 2: Database Version & Banner Grabbing
        flag2 = self.flags[2]["flag"]
        sql_statements.append(f"-- Challenge 2: Database Version & Banner Grabbing")
        sql_statements.append(f"-- Flag location: system_info table -> db_version column")
        sql_statements.append(f"INSERT INTO system_info (info_key, info_value) VALUES ('db_version', '{flag2}');\n")

        # ============================================================
        # PHASE 2: MISCONFIGURATION DISCOVERY
        # ============================================================
        sql_statements.append("\n-- ============================================================")
        sql_statements.append("-- PHASE 2: MISCONFIGURATION DISCOVERY")
        sql_statements.append("-- ============================================================\n")

        # Challenge 3: Weak Credentials Discovery
        flag3 = self.flags[3]["flag"]
        sql_statements.append(f"-- Challenge 3: Weak Credentials Discovery")
        sql_statements.append(f"-- Creates weak credential user and stores flag in users table")
        sql_statements.append(f"CREATE USER IF NOT EXISTS 'backup'@'%' IDENTIFIED BY 'backup123';")
        sql_statements.append(f"GRANT SELECT ON ctf_database.* TO 'backup'@'%';")
        sql_statements.append(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS welcome_flag VARCHAR(255);")
        sql_statements.append(f"UPDATE users SET welcome_flag = '{flag3}' WHERE username = 'john_doe';\n")

        # Challenge 4: Excessive Privileges Detection
        flag4 = self.flags[4]["flag"]
        sql_statements.append(f"-- Challenge 4: Excessive Privileges Detection")
        sql_statements.append(f"-- Creates table to store privilege audit findings")
        sql_statements.append(f"CREATE TABLE IF NOT EXISTS user_privileges (")
        sql_statements.append(f"    id INT AUTO_INCREMENT PRIMARY KEY,")
        sql_statements.append(f"    username VARCHAR(50),")
        sql_statements.append(f"    privilege_type VARCHAR(50),")
        sql_statements.append(f"    security_risk TEXT,")
        sql_statements.append(f"    discovery_flag VARCHAR(255)")
        sql_statements.append(f");")
        sql_statements.append(f"INSERT INTO user_privileges (username, privilege_type, security_risk, discovery_flag)")
        sql_statements.append(f"VALUES ('ctf_user', 'FILE', 'Can read any file from filesystem', '{flag4}');\n")

        # Challenge 5: Insecure Configuration Audit
        flag5 = self.flags[5]["flag"]
        sql_statements.append(f"-- Challenge 5: Insecure Configuration Audit")
        sql_statements.append(f"-- Creates config audit table")
        sql_statements.append(f"CREATE TABLE IF NOT EXISTS config_audit (")
        sql_statements.append(f"    id INT AUTO_INCREMENT PRIMARY KEY,")
        sql_statements.append(f"    config_name VARCHAR(100),")
        sql_statements.append(f"    config_value TEXT,")
        sql_statements.append(f"    risk_level VARCHAR(20),")
        sql_statements.append(f"    audit_flag VARCHAR(255)")
        sql_statements.append(f");")
        sql_statements.append(f"INSERT INTO config_audit (config_name, config_value, risk_level, audit_flag) VALUES")
        sql_statements.append(f"('secure_file_priv', '', 'CRITICAL', '{flag5}');\n")

        # ============================================================
        # PHASE 3: PRIVILEGE ESCALATION
        # ============================================================
        sql_statements.append("\n-- ============================================================")
        sql_statements.append("-- PHASE 3: PRIVILEGE ESCALATION")
        sql_statements.append("-- ============================================================\n")

        # Challenge 6: Horizontal Privilege Escalation
        flag6 = self.flags[6]["flag"]
        sql_statements.append(f"-- Challenge 6: Horizontal Privilege Escalation")
        sql_statements.append(f"-- Creates user_secrets table with other users' private data")
        sql_statements.append(f"CREATE TABLE IF NOT EXISTS user_secrets (")
        sql_statements.append(f"    id INT AUTO_INCREMENT PRIMARY KEY,")
        sql_statements.append(f"    user_id INT,")
        sql_statements.append(f"    private_data TEXT,")
        sql_statements.append(f"    secret_key VARCHAR(255)")
        sql_statements.append(f");")
        sql_statements.append(f"INSERT INTO user_secrets (user_id, private_data, secret_key) VALUES")
        sql_statements.append(f"(2, 'Jane Smith Private Documents', '{flag6}');\n")

        # Challenge 7: Vertical Privilege Escalation via Stored Procedures
        flag7 = self.flags[7]["flag"]
        sql_statements.append(f"-- Challenge 7: Vertical Privilege Escalation")
        sql_statements.append(f"-- Creates stored procedure with DEFINER=root (runs with elevated privileges)")
        sql_statements.append(f"""DELIMITER //
CREATE DEFINER=root@localhost PROCEDURE get_admin_flag()
    SQL SECURITY DEFINER
    COMMENT 'Admin-only procedure - vulnerable to privilege escalation'
BEGIN
    -- This procedure runs with root privileges due to DEFINER clause
    -- Regular users can call it and execute with elevated context
    SELECT '{flag7}' AS admin_flag, 'Privilege Escalation Successful' AS message;
END //
DELIMITER ;
""")
        sql_statements.append(f"GRANT EXECUTE ON PROCEDURE ctf_database.get_admin_flag TO 'ctf_user'@'%';\n")

        # ============================================================
        # PHASE 4: INJECTION ATTACKS
        # ============================================================
        sql_statements.append("\n-- ============================================================")
        sql_statements.append("-- PHASE 4: INJECTION ATTACKS")
        sql_statements.append("-- ============================================================\n")

        # Challenge 8: Authentication Bypass via SQL Injection
        flag8 = self.flags[8]["flag"]
        sql_statements.append(f"-- Challenge 8: Authentication Bypass via SQL Injection")
        sql_statements.append(f"-- Flag stored in admin_panel table (accessible after SQLi bypass)")
        sql_statements.append(f"INSERT INTO admin_panel (username, password, secret_key) VALUES")
        sql_statements.append(f"('admin', MD5('impossible_admin_password_2024!@#'), '{flag8}');\n")

        # Challenge 9: Blind SQL Injection & Data Exfiltration
        flag9 = self.flags[9]["flag"]
        sql_statements.append(f"-- Challenge 9: Blind SQL Injection")
        sql_statements.append(f"-- Adds hidden_flag column to products table")
        sql_statements.append(f"ALTER TABLE products ADD COLUMN IF NOT EXISTS hidden_flag VARCHAR(255);")
        sql_statements.append(f"UPDATE products SET hidden_flag = '{flag9}' WHERE id = 1;\n")

        # ============================================================
        # PHASE 5: KEY EXTRACTION (Master Challenge)
        # ============================================================
        sql_statements.append("\n-- ============================================================")
        sql_statements.append("-- PHASE 5: KEY EXTRACTION - Multi-Stage Attack")
        sql_statements.append("-- ============================================================\n")

        # Challenge 10: Master Key - Split across 3 locations
        flag10 = self.flags[10]["flag"]

        # Split the flag into 3 parts
        flag_clean = flag10.replace("FLAG{", "").replace("}", "")
        part_size = len(flag_clean) // 3
        part1 = flag_clean[:part_size]
        part2 = flag_clean[part_size:part_size*2]
        part3 = flag_clean[part_size*2:]

        sql_statements.append(f"-- Challenge 10: Master Key Extraction")
        sql_statements.append(f"-- Part 1: Stored in file (requires LOAD_FILE)")
        sql_statements.append(f"-- Part 2: Stored in audit_log (requires log analysis)")
        sql_statements.append(f"-- Part 3: Stored in trigger definition (requires trigger enumeration)")
        sql_statements.append(f"-- Final flag: FLAG{{part1_part2_part3}}\n")

        # Part 1: File reference for LOAD_FILE()
        sql_statements.append(f"INSERT INTO file_references (filename, content, file_type) VALUES")
        sql_statements.append(f"('/var/lib/mysql/secret_part1.txt', 'KEY_PART_1: {part1}', 'secret');\n")

        # Part 2: Audit log entry (encoded)
        sql_statements.append(f"INSERT INTO audit_log (action, flag, user_agent) VALUES")
        sql_statements.append(f"('master_key_fragment', 'KEY_PART_2: {part2}', 'Internal System');\n")

        # Part 3: Trigger with embedded flag
        sql_statements.append(f"""-- Part 3: Hidden in trigger definition
DELIMITER //
CREATE TRIGGER master_key_trigger
BEFORE INSERT ON user_logs
FOR EACH ROW
BEGIN
    -- Master Key Part 3: {part3}
    -- Combine all 3 parts to get the master flag
    SET @key_part3 = '{part3}';
END //
DELIMITER ;
""")

        sql_statements.append(f"\n-- Reconstruction hint")
        sql_statements.append(f"INSERT INTO audit_log (action, flag) VALUES")
        sql_statements.append(f"('reconstruction_hint', 'Combine: LOAD_FILE + audit_log + trigger = Master Key');\n")

        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(sql_statements))

        print(f"[OK] SQL init script saved to {output_file}")

    def generate_env_file(self, output_file=".env"):
        """Generate .env file with instance salt and passwords"""

        root_password = secrets.token_urlsafe(16)
        db_password = secrets.token_urlsafe(12)

        env_content = f"""# Auto-generated environment variables for Database Security CTF
# DO NOT COMMIT THIS FILE TO VERSION CONTROL

# Instance Configuration
INSTANCE_SALT={self.instance_salt}

# MySQL Configuration
MYSQL_ROOT_PASSWORD={root_password}
MYSQL_DATABASE=ctf_database
MYSQL_USER=ctf_user
MYSQL_PASSWORD={db_password}

# CTF Platform Configuration
CTF_SECRET_KEY={secrets.token_hex(32)}
CTF_ADMIN_PASSWORD={secrets.token_urlsafe(12)}

# Vulnerable Web App
WEB_SESSION_SECRET={secrets.token_hex(24)}
"""

        with open(output_file, 'w') as f:
            f.write(env_content)

        print(f"[OK] Environment file saved to {output_file}")
        print(f"\n[!] IMPORTANT: Keep this .env file secure!")
        print(f"    MySQL Root Password: {root_password}")
        print(f"    CTF User Password: {db_password}")


def main():
    print("=" * 60)
    print("Database Security CTF - Flag Generator")
    print("=" * 60)
    print()

    # Check if salt is provided via environment variable
    instance_salt = os.environ.get('INSTANCE_SALT')

    if instance_salt:
        print(f"[+] Using provided instance salt: {instance_salt[:8]}...")
    else:
        print(f"[+] Generating new instance salt...")

    # Initialize generator
    generator = FlagGenerator(instance_salt)

    print(f"[+] Instance Salt: {generator.instance_salt}\n")
    print("=" * 60)
    print("Generating Flags...")
    print("=" * 60)
    print()

    # Generate all flags
    generator.generate_all_flags()

    # Determine output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(output_dir)

    # Save outputs
    print("=" * 60)
    print("Saving Outputs...")
    print("=" * 60)
    print()

    generator.save_to_json(os.path.join(parent_dir, "flags.json"))
    generator.generate_sql_init(os.path.join(parent_dir, "mysql", "init", "02-flags.sql"))
    generator.generate_env_file(os.path.join(parent_dir, ".env"))

    print()
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the generated .env file")
    print("2. Run: docker-compose up -d")
    print("3. Access CTF Platform: http://localhost:5000")
    print("4. Access Vulnerable App: http://localhost:8080")
    print()


if __name__ == "__main__":
    main()
