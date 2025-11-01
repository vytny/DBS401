# 🚀 Quick Start Guide

Hướng dẫn khởi động nhanh Database Security CTF trong 5 phút!

## ✅ Prerequisites Check

Trước khi bắt đầu, đảm bảo bạn đã cài:
- ✅ Docker Desktop (đang chạy)
- ✅ Python 3.7+

## 🏃 Khởi Động Trong 3 Bước

### Bước 1: Mở Command Prompt

```cmd
cd C:\Users\noter\database-security-ctf
```

### Bước 2: Chạy Setup

```cmd
setup.bat
```

Script sẽ tự động:
- Generate flags ngẫu nhiên
- Tạo file .env với passwords
- Build Docker containers
- Start tất cả services

**Thời gian:** ~5-10 phút (lần đầu)

### Bước 3: Truy Cập

Sau khi setup xong, mở browser:

🎮 **CTF Platform:** http://localhost:5000
🌐 **Vulnerable App:** http://localhost:8080
🗄️ **MySQL:** `localhost:3306`

## 📝 Credentials

Xem file `.env` để lấy password:
```cmd
type .env
```

Copy `MYSQL_PASSWORD` để connect MySQL.

## 🎯 Bắt Đầu Chơi

1. Mở http://localhost:5000
2. Chọn **Challenge 1: Database Fingerprinting**
3. Click **"Show Hints"** để xem gợi ý
4. Thực hiện pentesting trên targets
5. Submit flag khi tìm được

## 🔧 Các Lệnh Hữu Ích

```bash
# Xem logs
docker-compose logs -f

# Stop containers
docker-compose down

# Restart
docker-compose restart

# Xem status
docker-compose ps

# Connect MySQL
mysql -h localhost -P 3306 -u ctf_user -p
# (nhập password từ .env file)
```

## 🆘 Troubleshooting

### Problem: Docker không chạy
**Solution:**
1. Mở Docker Desktop từ Start Menu
2. Chờ Docker khởi động (icon chuyển màu xanh)
3. Chạy lại `setup.bat`

### Problem: Port bị chiếm
**Solution:**
```cmd
# Check process đang dùng port
netstat -ano | findstr :3306
netstat -ano | findstr :5000
netstat -ano | findstr :8080

# Kill process (thay PID)
taskkill /PID <PID> /F
```

### Problem: Python lỗi
**Solution:**
```cmd
# Kiểm tra Python
python --version

# Install lại nếu cần
# Download: https://www.python.org/downloads/
```

## 📚 Next Steps

1. ✅ Setup xong? → Đọc [README.md](README.md) để hiểu chi tiết
2. 🔍 Bắt đầu pentest? → Xem [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md)
3. 💻 Code bị lỗi? → Check Docker logs: `docker-compose logs`

## 🎓 Cho Bạn Cùng Nhóm (Pentester)

Sau khi môi trường đã chạy:

1. **Đọc hướng dẫn pentest:** [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md)
2. **Install tools:**
   - nmap: https://nmap.org/download.html
   - sqlmap: `pip install sqlmap-python`
   - Burp Suite: https://portswigger.net/burp/communitydownload

3. **Bắt đầu từ Challenge 1**
4. **Document mọi bước**
5. **Use AI tools** (ChatGPT, Claude) để tối ưu

## 🎬 Demo Flow

```bash
# 1. Scan target
nmap -sV localhost

# 2. Check web app
curl http://localhost:8080

# 3. Try SQL injection
# Vào http://localhost:8080 → Login
# Username: admin' OR '1'='1' --

# 4. Connect MySQL
mysql -h localhost -P 3306 -u ctf_user -p

# 5. Explore database
SHOW DATABASES;
USE ctf_database;
SHOW TABLES;
SELECT * FROM system_info;

# 6. Find flags và submit vào http://localhost:5000
```

## 📊 Progress Tracking

| Step | Description | Status |
|------|-------------|--------|
| 1 | Install Docker Desktop | ⬜ |
| 2 | Install Python | ⬜ |
| 3 | Run setup.bat | ⬜ |
| 4 | Access CTF Platform | ⬜ |
| 5 | Solve Challenge 1 | ⬜ |
| 6 | Solve all 10 challenges | ⬜ |
| 7 | Write report | ⬜ |

## 💡 Tips

- 🔍 **Start simple:** Bắt đầu từ Challenge 1, không skip
- 📝 **Document everything:** Screenshot, save commands
- 🤖 **Use AI:** ChatGPT/Claude cho hints và explanation
- 🔄 **Retry:** Mỗi lần chạy setup.bat sẽ tạo flags mới
- 👥 **Ask for help:** Đọc hints trong mỗi challenge

## 🎯 Goals Checklist

Phần của bạn (Setup):
- ✅ Tạo được Docker environment
- ✅ MySQL chạy với vulnerabilities
- ✅ Web app vulnerable hoạt động
- ✅ CTF platform validate flags
- ✅ Flags generate ngẫu nhiên

Phần bạn cùng nhóm (Pentest):
- ⬜ Complete 10/10 challenges
- ⬜ Use AI tools trong workflow
- ⬜ Follow pentesting methodology
- ⬜ Document findings
- ⬜ Create professional report

## 🎉 Done!

Nếu mọi thứ chạy smooth:
- CTF Platform: http://localhost:5000 ✅
- Vulnerable App: http://localhost:8080 ✅
- MySQL: localhost:3306 ✅

**Have fun hacking! 🚀**

---

Need help? Check:
- [README.md](README.md) - Full documentation
- [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md) - Pentest guide
- Docker logs: `docker-compose logs -f`
