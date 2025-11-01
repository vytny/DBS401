<?php
$error = '';
$admin_data = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // VULNERABILITY: SQL Injection - Admin authentication bypass
    $admin_data = checkAdminCredentials($username, $password);

    if ($admin_data) {
        $_SESSION['admin_id'] = $admin_data['id'];
        $_SESSION['admin_username'] = $admin_data['username'];
        $_SESSION['is_admin'] = true;
    } else {
        $error = "Invalid admin credentials!";
    }
}

// Check if already logged in as admin
if (isset($_SESSION['is_admin']) && $_SESSION['is_admin']) {
    $admin_id = $_SESSION['admin_id'];
    $result = executeQuery("SELECT * FROM admin_panel WHERE id = $admin_id");
    if ($result && $result->num_rows > 0) {
        $admin_data = $result->fetch_assoc();
    }
}
?>

<?php if ($admin_data): ?>
    <!-- Admin Dashboard -->
    <div class="admin-dashboard">
        <h2>🔐 Admin Dashboard</h2>

        <div class="alert alert-success">
            Welcome, <?php echo htmlspecialchars($admin_data['username']); ?>!
        </div>

        <div class="admin-panels">
            <div class="admin-panel">
                <h3>Your Admin Information</h3>
                <table class="admin-table">
                    <tr>
                        <th>ID:</th>
                        <td><?php echo htmlspecialchars($admin_data['id']); ?></td>
                    </tr>
                    <tr>
                        <th>Username:</th>
                        <td><?php echo htmlspecialchars($admin_data['username']); ?></td>
                    </tr>
                    <tr>
                        <th>Secret Key:</th>
                        <td><code class="secret-key"><?php echo htmlspecialchars($admin_data['secret_key']); ?></code></td>
                    </tr>
                    <tr>
                        <th>Last Login:</th>
                        <td><?php echo $admin_data['last_login'] ? date('Y-m-d H:i:s', strtotime($admin_data['last_login'])) : 'Never'; ?></td>
                    </tr>
                </table>
            </div>

            <div class="admin-panel">
                <h3>System Statistics</h3>
                <?php
                $user_count = executeQuery("SELECT COUNT(*) as count FROM users");
                $product_count = executeQuery("SELECT COUNT(*) as count FROM products");
                $comment_count = executeQuery("SELECT COUNT(*) as count FROM comments");

                $users = $user_count ? $user_count->fetch_assoc()['count'] : 0;
                $products = $product_count ? $product_count->fetch_assoc()['count'] : 0;
                $comments = $comment_count ? $comment_count->fetch_assoc()['count'] : 0;
                ?>
                <ul class="stats-list">
                    <li>Total Users: <strong><?php echo $users; ?></strong></li>
                    <li>Total Products: <strong><?php echo $products; ?></strong></li>
                    <li>Total Comments: <strong><?php echo $comments; ?></strong></li>
                </ul>
            </div>

            <div class="admin-panel">
                <h3>Database Information</h3>
                <?php
                $db_result = executeQuery("SELECT DATABASE() as db_name, VERSION() as version, USER() as current_user");
                if ($db_result) {
                    $db_info = $db_result->fetch_assoc();
                ?>
                <ul class="stats-list">
                    <li>Database: <strong><?php echo htmlspecialchars($db_info['db_name']); ?></strong></li>
                    <li>Version: <strong><?php echo htmlspecialchars($db_info['version']); ?></strong></li>
                    <li>Current User: <strong><?php echo htmlspecialchars($db_info['current_user']); ?></strong></li>
                </ul>
                <?php } ?>
            </div>

            <div class="admin-panel">
                <h3>Recent Activity</h3>
                <?php
                $logs = executeQuery("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 5");
                if ($logs && $logs->num_rows > 0):
                ?>
                <table class="activity-table">
                    <thead>
                        <tr>
                            <th>Action</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while($log = $logs->fetch_assoc()): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($log['action']); ?></td>
                            <td><?php echo date('Y-m-d H:i:s', strtotime($log['timestamp'])); ?></td>
                        </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
                <?php else: ?>
                <p>No recent activity.</p>
                <?php endif; ?>
            </div>
        </div>

        <div class="admin-actions">
            <a href="logout.php" class="btn btn-danger">Logout</a>
        </div>
    </div>

<?php else: ?>
    <!-- Admin Login Form -->
    <div class="admin-login-container">
        <h2>🔐 Admin Login</h2>

        <div class="warning-box">
            <strong>⚠️ Authorized Personnel Only</strong>
            <p>This area is restricted to administrators. Unauthorized access is prohibited.</p>
        </div>

        <?php if ($error): ?>
            <div class="alert alert-error"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>

        <form method="POST" action="" class="admin-form">
            <div class="form-group">
                <label for="username">Admin Username:</label>
                <input type="text" id="username" name="username" required>
            </div>

            <div class="form-group">
                <label for="password">Admin Password:</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn btn-primary">Login as Admin</button>
        </form>

        <div class="hint-box">
            <p><small>💡 Hint: The admin password is impossible to guess... or is it?</small></p>
        </div>
    </div>
<?php endif; ?>

<style>
.admin-login-container {
    max-width: 500px;
    margin: 50px auto;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.admin-dashboard {
    padding: 20px;
}

.warning-box {
    background: #fff3cd;
    border: 2px solid #ffc107;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.admin-panels {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.admin-panel {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.admin-panel h3 {
    margin-top: 0;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
}

.admin-table th {
    text-align: left;
    padding: 10px;
    background: #f8f9fa;
    width: 40%;
}

.admin-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.secret-key {
    background: #e9ecef;
    padding: 5px 10px;
    border-radius: 4px;
    font-family: monospace;
    color: #d63384;
    font-weight: bold;
}

.stats-list {
    list-style: none;
    padding: 0;
}

.stats-list li {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}

.activity-table {
    width: 100%;
    border-collapse: collapse;
}

.activity-table th {
    background: #f8f9fa;
    padding: 10px;
    text-align: left;
    border-bottom: 2px solid #dee2e6;
}

.activity-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.admin-actions {
    margin-top: 30px;
    text-align: center;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn-danger:hover {
    background: #c82333;
}

.hint-box {
    margin-top: 20px;
    text-align: center;
    color: #666;
}
</style>
