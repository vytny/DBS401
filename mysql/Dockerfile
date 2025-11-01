FROM mysql:8.0-debian

# Copy custom MySQL configuration
COPY my.cnf /etc/mysql/conf.d/custom.cnf

# ⚠️ Không tạo /var/lib/mysql/secrets tại đây
# Nếu cần thư mục này, hãy tạo bằng script trong ./mysql/init sau khi DB đã init

EXPOSE 3306

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD mysqladmin ping -h localhost -u root -p$MYSQL_ROOT_PASSWORD || exit 1
