<?php
$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // VULNERABILITY: SQL Injection via getUserByCredentials
    $user = getUserByCredentials($username, $password);

    if ($user) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        $_SESSION['role'] = $user['role'];

        // Log the login action
        logUserAction($user['id'], 'login', $_SERVER['REMOTE_ADDR']);

        $success = "Login successful! Redirecting...";
        header("Refresh: 2; url=index.php?page=profile");
    } else {
        $error = "Invalid username or password!";
    }
}
?>

<div class="login-container">
    <h2>Login to SecureShop</h2>

    <?php if ($error): ?>
        <div class="alert alert-error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <?php if ($success): ?>
        <div class="alert alert-success"><?php echo htmlspecialchars($success); ?></div>
    <?php endif; ?>

    <form method="POST" action="" class="login-form">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>

        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>

        <button type="submit" class="btn btn-primary">Login</button>
    </form>

    <div class="hints">
        <h3>Test Accounts:</h3>
        <ul>
            <li>Username: <code>guest</code> | Password: <code>guest</code></li>
            <li>Username: <code>john_doe</code> | Password: <code>password123</code></li>
        </ul>
        <p><small>Or try to bypass authentication... 😉</small></p>
    </div>

    <div class="admin-link">
        <p>Are you an admin? <a href="index.php?page=admin">Admin Login</a></p>
    </div>
</div>

<style>
.login-container {
    max-width: 500px;
    margin: 50px auto;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.login-form {
    margin-top: 20px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-primary:hover {
    background: #0056b3;
}

.hints {
    margin-top: 30px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 4px;
}

.hints code {
    background: #e9ecef;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: monospace;
}

.admin-link {
    margin-top: 20px;
    text-align: center;
}

.alert {
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 4px;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
</style>
