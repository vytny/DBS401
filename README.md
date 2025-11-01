# Database Security CTF Lab

Một môi trường CTF (Capture The Flag) được thiết kế để học và thực hành Database Penetration Testing với MySQL.

## 📋 Tổng Quan

Dự án này bao gồm:
- **MySQL Database** với các lỗ hổng bảo mật được thiết kế
- **Vulnerable Web Application** (PHP) để khai thác SQL Injection
- **CTF Platform** (Python Flask) để submit flags và theo dõi tiến độ
- **10 Challenges** theo đúng quy trình Penetration Testing

## 🎯 Mục Tiêu Học Tập

1. Hiểu về các lỗ hổng Database Security phổ biến
2. Thực hành Penetration Testing theo chuẩn quy trình
3. Sử dụng công cụ AI trong Security Testing
4. Phát triển kỹ năng SQL Injection và Post-Exploitation

## 🛠️ Yêu Cầu Hệ Thống

### Windows (Khuyến nghị cho dự án này):
- Windows 10/11
- Docker Desktop for Windows (với WSL2)
- Python 3.7 trở lên
- 4GB RAM trở lên
- 10GB ổ cứng trống

### Công cụ Pentesting (Tùy chọn):
- nmap
- sqlmap
- Burp Suite Community
- MySQL Client
- Python với requests library

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Clone hoặc Download Project

```bash
cd C:\Users\noter
git clone <repository-url> database-security-ctf
cd database-security-ctf
```

### Bước 2: Cài Đặt Docker Desktop

1. Download Docker Desktop từ: https://www.docker.com/products/docker-desktop
2. Cài đặt và khởi động Docker Desktop
3. Đảm bảo Docker đang chạy (kiểm tra system tray)

### Bước 3: Set Up
Chạy file generate_flags
**Trên Windows:**
```cmd
C:\Users\VyVa\Documents\FA25\DBS401\database-security-ctf\flag-generator> python3 generate_flags.py
```

- Generate flags ngẫu nhiên cho instance của bạn
- Sinh file `.env` với credentials

Build và start Docker containers:
(1) 
```cmd
docker compose build
```
Kết quả 
```cmd
[+] Building 3/3
 ✔ ctf-platform    Built                                                                                           0.0s
 ✔ mysql           Built                                                                                           0.0s
 ✔ vulnerable-web  Built  
```

(2)
```cmd
docker compose up -d
```
Kết quả
```cmd
[+] Running 5/5
 ✔ Network database-security-ctf_ctf-network  Created                                                              0.1s
 ✔ Volume "database-security-ctf_mysql-data"  Created                                                              0.0s
 ✔ Container ctf-mysql                        Healthy                                                             21.4s
 ✔ Container ctf-vulnerable-web               Started                                                             21.6s
 ✔ Container ctf-platform                     Started                                                             21.6s
```

### Bước 4: Truy Cập Các Services

Sau khi setup hoàn tất:

- **CTF Platform:** http://localhost:5000
- **Vulnerable Web App:** http://localhost:8080
- **MySQL Database:** `localhost:3306`

## 📚 Cấu Trúc Project

```
database-security-ctf/
├── docker-compose.yml          # Docker orchestration
├── setup.bat                   # Windows setup script
├── .env                        # Environment variables (auto-generated)
├── flags.json                  # Generated flags (auto-generated)
│
├── flag-generator/             # Flag generation system
│   └── generate_flags.py       # Python script to generate unique flags
│
├── mysql/                      # MySQL Database container
│   ├── Dockerfile
│   ├── my.cnf                  # MySQL configuration (intentionally weak)
│   └── init/
│       ├── 01-schema.sql       # Database schema
│       └── 02-flags.sql        # Flags injection (auto-generated)
│
├── vulnerable-web/             # Vulnerable PHP Application
│   ├── Dockerfile
│   └── app/
│       ├── index.php           # Main entry point
│       ├── config.php          # Configuration
│       ├── db.php              # Database functions (vulnerable)
│       ├── style.css           # Styling
│       └── pages/              # Application pages
│           ├── home.php
│           ├── login.php
│           ├── products.php
│           ├── search.php
│           └── admin.php
│
└── ctf-platform/               # CTF Platform (Flask)
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py                  # Main Flask application
    ├── templates/              # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── challenge.html
    │   ├── scoreboard.html
    │   └── about.html
    └── static/                 # Static files
        ├── css/style.css
        └── js/main.js
```

## 🎮 Cách Chơi

### 1. Truy cập CTF Platform

Mở trình duyệt và truy cập: http://localhost:5000

### 2. Chọn Challenge

10 challenges được chia thành 4 categories:
- **Reconnaissance** (2 challenges)
- **Enumeration** (2 challenges)
- **Exploitation** (3 challenges)
- **Post-Exploitation** (3 challenges)

### 3. Thực Hiện Pentesting

Sử dụng các công cụ để tấn công:
- Target web: http://localhost:8080
- MySQL: `mysql -h localhost -P 3306 -u ctf_user -p`

### 4. Tìm Flags

Mỗi challenge có flag theo format: `FLAG{hash_string}`

### 5. Submit Flags

Submit flags vào CTF Platform để ghi điểm

## 🔍 Danh Sách Challenges

### Challenge 1: Database Fingerprinting (100 pts)
**Category:** Reconnaissance
**Objective:** Xác định loại database và version
**Hint:** Sử dụng nmap hoặc kết nối trực tiếp MySQL

### Challenge 2: Service Enumeration (100 pts)
**Category:** Reconnaissance
**Objective:** Liệt kê các services đang chạy
**Hint:** Check system_info table

### Challenge 3: Database Schema Discovery (150 pts)
**Category:** Enumeration
**Objective:** Tìm hidden databases
**Hint:** SHOW DATABASES

### Challenge 4: User Enumeration (150 pts)
**Category:** Enumeration
**Objective:** Tìm MySQL users
**Hint:** mysql.user table

### Challenge 5: SQL Injection - Authentication Bypass (200 pts)
**Category:** Exploitation
**Objective:** Bypass admin login
**Hint:** ' OR '1'='1' --

### Challenge 6: Blind SQL Injection (250 pts)
**Category:** Exploitation
**Objective:** Extract hidden data
**Hint:** UNION-based injection

### Challenge 7: Local File Read (250 pts)
**Category:** Exploitation
**Objective:** Đọc files từ server
**Hint:** LOAD_FILE() function

### Challenge 8: Privilege Escalation (300 pts)
**Category:** Post-Exploitation
**Objective:** Access admin procedures
**Hint:** SHOW PROCEDURE STATUS

### Challenge 9: Backdoor Detection (200 pts)
**Category:** Post-Exploitation
**Objective:** Tìm backdoor trigger
**Hint:** SHOW TRIGGERS

### Challenge 10: Log Analysis (150 pts)
**Category:** Post-Exploitation
**Objective:** Phân tích logs
**Hint:** audit_log table

## 🤖 Tích Hợp AI Tools

### Sử dụng ChatGPT/Claude:

1. **Phân tích Error Messages:**
```
Prompt: "Analyze this SQL error and suggest exploitation: [error_message]"
```

2. **Generate SQLi Payloads:**
```
Prompt: "Generate SQL injection payloads for MySQL authentication bypass"
```

3. **Blind SQLi Optimization:**
```
Prompt: "Optimize this blind SQL injection script for faster extraction"
```

### Python Script với OpenAI API:

```python
import openai

def generate_payload(context):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Generate SQLi payload: {context}"
        }]
    )
    return response.choices[0].message.content
```

## 🔧 Quản Lý Containers

### Xem logs:
```bash
docker-compose logs -f
docker-compose logs mysql
docker-compose logs vulnerable-web
docker-compose logs ctf-platform
```

### Stop containers:
```bash
docker-compose down
```

### Restart containers:
```bash
docker-compose restart
```

### Rebuild sau khi thay đổi code:
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Xem container status:
```bash
docker-compose ps
```

### Truy cập MySQL shell:
```bash
docker exec -it ctf-mysql mysql -u root -p
# Password: check .env file MYSQL_ROOT_PASSWORD
```

## 📝 Database Credentials

Check file `.env` (được tạo tự động) để lấy credentials:

```
MYSQL_ROOT_PASSWORD=<random>
MYSQL_DATABASE=ctf_database
MYSQL_USER=ctf_user
MYSQL_PASSWORD=<random>
```

### Connect MySQL từ máy local:

```bash
mysql -h localhost -P 3306 -u ctf_user -p
# Enter password from .env
```

## 🛡️ Quy Trình Pentesting Đề Xuất

### Phase 1: Reconnaissance
```bash
# Port scan
nmap -sV -p- localhost

# Banner grab
nc localhost 3306
```

### Phase 2: Enumeration
```bash
# Connect to MySQL
mysql -h localhost -P 3306 -u ctf_user -p

# Enumerate databases
SHOW DATABASES;

# Enumerate tables
USE ctf_database;
SHOW TABLES;
```

### Phase 3: Exploitation
```bash
# SQLMap automated scan
sqlmap -u "http://localhost:8080/index.php?page=login" \
       --data="username=admin&password=test" \
       --dbs

# Manual SQLi testing
# Try: admin' OR '1'='1' --
```

### Phase 4: Post-Exploitation
```sql
-- Check stored procedures
SHOW PROCEDURE STATUS WHERE Db = 'ctf_database';

-- Check triggers
SHOW TRIGGERS FROM ctf_database;

-- Read logs
SELECT * FROM audit_log;
```

## ⚠️ Lưu Ý Quan Trọng

### Security Warnings:

1. **CHỈ SỬ DỤNG CHO HỌC TẬP**
   - Môi trường này có lỗ hổng bảo mật nghiêm trọng
   - KHÔNG deploy lên môi trường production
   - KHÔNG expose ra public network

2. **Docker Ports:**
   - Các ports chỉ bind trên localhost
   - Nếu cần test từ máy khác, cấu hình firewall cẩn thận

3. **Passwords:**
   - File `.env` chứa passwords ngẫu nhiên
   - Không commit `.env` vào Git
   - Mỗi lần chạy setup.bat sẽ tạo passwords mới

### Troubleshooting:

**Problem:** Docker không start
```
Solution:
1. Kiểm tra Docker Desktop đang chạy
2. Restart Docker Desktop
3. Check: docker info
```

**Problem:** Port đã được sử dụng
```
Solution:
1. Stop các services đang dùng port 3306, 5000, 8080
2. Hoặc sửa ports trong docker-compose.yml
```

**Problem:** MySQL không kết nối được
```
Solution:
1. Check logs: docker-compose logs mysql
2. Wait thêm vài giây cho MySQL khởi động
3. Verify: docker-compose ps
```

**Problem:** Flags không được generate
```
Solution:
1. cd flag-generator
2. python generate_flags.py
3. Check file flags.json được tạo
```

## 🎓 Dành Cho Giảng Viên

### Tùy Chỉnh Challenges:

Edit file `ctf-platform/app.py` để thay đổi:
- Số điểm của challenges
- Mô tả challenges
- Hints

### Reset Environment:

```bash
docker-compose down -v
python flag-generator/generate_flags.py
docker-compose up -d
```

### Xem Progress của Students:

Access CTF Platform và check scoreboard

## 📖 Tài Liệu Tham Khảo

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [MySQL Security Best Practices](https://dev.mysql.com/doc/refman/8.0/en/security.html)
- [sqlmap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)

## 👥 Credits

Dự án được phát triển cho môn Database Security
Educational Purpose Only

## 📄 License

MIT License - For Educational Use Only

## 🤝 Đóng Góp

Nếu tìm thấy bugs hoặc có suggestions:
1. Tạo Issue
2. Submit Pull Request
3. Contact: [your-email]

---

**Have fun hacking! 🚀**

Remember: Always hack ethically and legally! 🛡️
