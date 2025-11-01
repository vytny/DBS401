#!/usr/bin/env python3
"""
AI-Powered MySQL Password Wordlist Generator
For Challenge 3: Weak Credentials Discovery

This script uses AI to generate context-aware password wordlists
specifically for MySQL environments.
"""

import argparse
import os
import sys

try:
    import openai
except ImportError:
    print("[!] OpenAI library not installed. Run: pip install openai")
    sys.exit(1)


class AIWordlistGenerator:
    def __init__(self, api_key=None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass --api-key")

        openai.api_key = self.api_key

    def generate_mysql_wordlist(self, count=50):
        """Generate MySQL-specific password wordlist using AI"""

        prompt = f"""Generate {count} common weak passwords specifically for MySQL databases.
Include:
- Default MySQL passwords
- Common patterns like: mysql, password, admin123
- Variations of 'root', 'admin', 'backup', 'test'
- Empty password (represented as <EMPTY>)
- Same as username patterns
- Sequential numbers (123456, etc.)
- Common company/database names

Format: One password per line.
Output ONLY the passwords, no explanations."""

        print(f"[*] Generating {count} MySQL passwords using AI...")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a security researcher generating password wordlists for authorized penetration testing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )

            passwords = response.choices[0].message.content.strip().split('\n')
            passwords = [p.strip() for p in passwords if p.strip()]

            return passwords

        except Exception as e:
            print(f"[!] Error calling OpenAI API: {e}")
            print("[*] Falling back to basic wordlist...")
            return self.get_fallback_wordlist()

    def get_fallback_wordlist(self):
        """Fallback wordlist if AI fails"""
        return [
            "",  # Empty password
            "mysql",
            "password",
            "admin",
            "root",
            "backup123",
            "test",
            "admin123",
            "password123",
            "mysql123",
            "root123",
            "toor",
            "backup",
            "database",
            "db",
            "changeme",
            "default",
            "123456",
            "qwerty",
            "letmein"
        ]

    def save_wordlist(self, passwords, output_file):
        """Save wordlist to file"""
        with open(output_file, 'w') as f:
            for password in passwords:
                if password == "<EMPTY>":
                    f.write('\n')  # Empty line for empty password
                else:
                    f.write(f"{password}\n")

        print(f"[+] Wordlist saved to {output_file}")
        print(f"[+] Total passwords: {len(passwords)}")


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered MySQL Password Wordlist Generator",
        epilog="Example: python wordlist_generator.py --api-key sk-... --output mysql_pass.txt"
    )

    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('--output', '-o', default='mysql_passwords.txt', help='Output file (default: mysql_passwords.txt)')
    parser.add_argument('--count', '-c', type=int, default=50, help='Number of passwords to generate (default: 50)')
    parser.add_argument('--fallback', action='store_true', help='Use fallback wordlist without AI')

    args = parser.parse_args()

    print("=" * 60)
    print("AI-Powered MySQL Wordlist Generator")
    print("For Challenge 3: Weak Credentials Discovery")
    print("=" * 60)
    print()

    if args.fallback:
        print("[*] Using fallback wordlist (no AI)")
        generator = AIWordlistGenerator.__new__(AIWordlistGenerator)
        passwords = generator.get_fallback_wordlist()
    else:
        try:
            generator = AIWordlistGenerator(api_key=args.api_key)
            passwords = generator.generate_mysql_wordlist(count=args.count)
        except ValueError as e:
            print(f"[!] {e}")
            print("[*] Use --fallback flag to generate basic wordlist without AI")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error: {e}")
            sys.exit(1)

    if passwords:
        generator.save_wordlist(passwords, args.output)
        print()
        print("Next steps:")
        print(f"1. Use with hydra: hydra -l backup -P {args.output} mysql://localhost")
        print(f"2. Try each password: mysql -h localhost -u backup -p<password>")
        print(f"3. Check users table after successful login for the flag")


if __name__ == "__main__":
    main()
