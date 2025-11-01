<?php
/**
 * User Profile Page - VULNERABLE VERSION
 * For Challenge 6: Horizontal Privilege Escalation
 *
 * VULNERABILITY: SQL Injection via user_id parameter
 * Allows accessing other users' private data
 */

// VULNERABILITY: Allow specifying user_id via GET parameter
// This enables horizontal privilege escalation
$user_id = isset($_GET['user_id']) ? $_GET['user_id'] : (isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 1);

// VULNERABILITY: Direct use of user input in SQL query without sanitization
$query = "SELECT u.id, u.username, u.email, u.role, u.created_at, us.private_data, us.secret_key, us.access_level
          FROM users u
          LEFT JOIN user_secrets us ON u.id = us.user_id
          WHERE u.id = $user_id";

if (DEBUG_MODE) {
    echo "<!-- DEBUG: Profile Query: " . htmlspecialchars($query) . " -->\n";
}

$result = executeQuery($query);

if ($result && $result->num_rows > 0) {
    $user = $result->fetch_assoc();
} else {
    $user = null;
}
?>

<div class="profile-container">
    <h2>👤 User Profile</h2>

    <?php if (DEBUG_MODE): ?>
    <div class="debug-info">
        <strong>🔍 DEBUG MODE ENABLED</strong><br>
        Viewing profile for user_id = <strong><?= htmlspecialchars($user_id) ?></strong><br>
        <em>Hint for Challenge 6: Try changing the user_id parameter!</em>
    </div>
    <?php endif; ?>

    <?php if ($user): ?>
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">
                    <?= strtoupper(substr($user['username'], 0, 1)) ?>
                </div>
                <div class="profile-info">
                    <h3><?= htmlspecialchars($user['username']) ?></h3>
                    <span class="role-badge"><?= htmlspecialchars($user['role']) ?></span>
                </div>
            </div>

            <div class="profile-details">
                <div class="detail-row">
                    <span class="detail-label">User ID:</span>
                    <span class="detail-value"><?= htmlspecialchars($user['id']) ?></span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value"><?= htmlspecialchars($user['email']) ?></span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Role:</span>
                    <span class="detail-value"><?= htmlspecialchars($user['role']) ?></span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Member Since:</span>
                    <span class="detail-value"><?= date('F d, Y', strtotime($user['created_at'])) ?></span>
                </div>
            </div>

            <?php if ($user['private_data']): ?>
            <div class="private-section">
                <h4>🔒 Private Information</h4>
                <div class="access-badge">
                    Access Level: <span class="badge-<?= htmlspecialchars($user['access_level']) ?>">
                        <?= htmlspecialchars($user['access_level']) ?>
                    </span>
                </div>
                <div class="private-data">
                    <?= nl2br(htmlspecialchars($user['private_data'])) ?>
                </div>

                <?php if ($user['secret_key']): ?>
                <div class="secret-key-section">
                    <h5>🎯 Secret Key Found!</h5>
                    <div class="secret-key-box">
                        <code><?= htmlspecialchars($user['secret_key']) ?></code>
                    </div>
                    <p class="success-hint">
                        ✅ This looks like a FLAG! Submit it to the CTF platform.
                    </p>
                </div>
                <?php endif; ?>
            </div>
            <?php else: ?>
            <div class="info-message">
                ℹ️ This user has no private data stored.
            </div>
            <?php endif; ?>

            <div class="quick-nav">
                <h4>Quick Navigation</h4>
                <div class="user-buttons">
                    <a href="?page=profile&user_id=1" class="user-btn">User 1</a>
                    <a href="?page=profile&user_id=2" class="user-btn">User 2</a>
                    <a href="?page=profile&user_id=3" class="user-btn">User 3</a>
                    <a href="?page=profile&user_id=4" class="user-btn">User 4</a>
                </div>
            </div>

            <?php if (DEBUG_MODE): ?>
            <div class="pentest-hints">
                <h4>🎓 Penetration Testing Hints:</h4>
                <ul>
                    <li><strong>IDOR Vulnerability:</strong> Notice the user_id parameter in URL</li>
                    <li><strong>Horizontal Privilege Escalation:</strong> You can view other users' profiles</li>
                    <li><strong>Objective:</strong> Find a user with a secret_key value</li>
                    <li><strong>Technique:</strong> Try different user_id values (1-10)</li>
                    <li><strong>Advanced:</strong> Use UNION injection: <code>?page=profile&user_id=1 UNION SELECT ...</code></li>
                    <li><strong>Tools:</strong> Burp Suite Intruder can automate user_id enumeration</li>
                </ul>
            </div>
            <?php endif; ?>
        </div>

    <?php else: ?>
        <div class="error-box">
            <h3>❌ User Not Found</h3>
            <p>No user found with ID: <strong><?= htmlspecialchars($user_id) ?></strong></p>
            <p>Try a different user_id value.</p>

            <?php if (DEBUG_MODE && $conn->error): ?>
            <div class="sql-error">
                <strong>SQL Error:</strong>
                <pre><?= htmlspecialchars($conn->error) ?></pre>
                <strong>Query:</strong>
                <pre><?= htmlspecialchars($query) ?></pre>
            </div>
            <?php endif; ?>
        </div>
    <?php endif; ?>
</div>

<style>
.profile-container {
    max-width: 800px;
    margin: 30px auto;
    padding: 20px;
}

.debug-info {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border-left: 4px solid #ffc107;
    padding: 15px 20px;
    margin-bottom: 20px;
    border-radius: 5px;
    font-size: 14px;
}

.profile-card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    overflow: hidden;
    margin-bottom: 20px;
}

.profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40px;
    display: flex;
    align-items: center;
    gap: 25px;
    color: white;
}

.profile-avatar {
    width: 90px;
    height: 90px;
    background: rgba(255,255,255,0.25);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    font-weight: bold;
    border: 3px solid rgba(255,255,255,0.5);
}

.profile-info h3 {
    margin: 0 0 10px 0;
    font-size: 28px;
}

.role-badge {
    background: rgba(255,255,255,0.3);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.profile-details {
    padding: 30px;
    background: #f8f9fa;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #dee2e6;
}

.detail-row:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 600;
    color: #495057;
}

.detail-value {
    color: #212529;
}

.private-section {
    padding: 30px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-top: 3px solid #3b82f6;
}

.private-section h4 {
    margin: 0 0 15px 0;
    color: #1e40af;
}

.access-badge {
    margin-bottom: 15px;
    font-size: 14px;
}

[class^="badge-"] {
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 11px;
}

.badge-private {
    background: #dc3545;
    color: white;
}

.badge-public {
    background: #28a745;
    color: white;
}

.private-data {
    background: white;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #bfdbfe;
    line-height: 1.6;
    color: #1e40af;
}

.secret-key-section {
    margin-top: 20px;
    padding: 20px;
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border: 2px solid #f59e0b;
    border-radius: 8px;
}

.secret-key-section h5 {
    margin: 0 0 15px 0;
    color: #92400e;
    font-size: 18px;
}

.secret-key-box {
    background: #ffffff;
    padding: 20px;
    border-radius: 6px;
    border: 2px dashed #f59e0b;
    margin-bottom: 15px;
}

.secret-key-box code {
    color: #dc2626;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Courier New', monospace;
    word-break: break-all;
}

.success-hint {
    margin: 10px 0 0 0;
    color: #15803d;
    font-weight: 600;
    font-size: 14px;
}

.info-message {
    padding: 20px;
    text-align: center;
    color: #6c757d;
    font-style: italic;
}

.quick-nav {
    padding: 25px 30px;
    background: white;
    border-top: 1px solid #dee2e6;
}

.quick-nav h4 {
    margin: 0 0 15px 0;
    font-size: 16px;
    color: #495057;
}

.user-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.user-btn {
    padding: 10px 20px;
    background: #6c757d;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-size: 14px;
    transition: all 0.3s;
}

.user-btn:hover {
    background: #5a6268;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.pentest-hints {
    padding: 25px 30px;
    background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
    border-top: 3px solid #8b5cf6;
}

.pentest-hints h4 {
    margin: 0 0 15px 0;
    color: #5b21b6;
}

.pentest-hints ul {
    margin: 0;
    padding-left: 20px;
}

.pentest-hints li {
    margin: 10px 0;
    color: #6d28d9;
    line-height: 1.6;
}

.pentest-hints code {
    background: rgba(255,255,255,0.7);
    padding: 3px 8px;
    border-radius: 4px;
    color: #dc2626;
    font-size: 13px;
}

.error-box {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
}

.error-box h3 {
    color: #dc3545;
    margin-bottom: 15px;
}

.sql-error {
    margin-top: 20px;
    padding: 20px;
    background: #f8d7da;
    border: 1px solid #f5c2c7;
    border-radius: 6px;
    text-align: left;
}

.sql-error pre {
    background: white;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 13px;
    margin: 10px 0;
}
</style>
