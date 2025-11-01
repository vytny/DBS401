#!/bin/bash
set -e

echo "Creating /var/lib/mysql/secrets directory..."
mkdir -p /var/lib/mysql/secrets
chown -R mysql:mysql /var/lib/mysql/secrets
chmod 700 /var/lib/mysql/secrets
echo "Secrets directory created successfully."