<?php
// Database Configuration
define('DB_HOST', getenv('DB_HOST') ?: 'mysql');
define('DB_USER', getenv('DB_USER') ?: 'ctf_user');
define('DB_PASSWORD', getenv('DB_PASSWORD') ?: 'password');
define('DB_NAME', getenv('DB_NAME') ?: 'ctf_database');

// Session Configuration
define('SESSION_SECRET', getenv('SESSION_SECRET') ?: 'change_this_secret');

// Application Settings
define('DEBUG_MODE', true); // Intentionally enabled for error disclosure
define('ITEMS_PER_PAGE', 10);

// Error Reporting (intentionally verbose for CTF)
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Timezone
date_default_timezone_set('UTC');
?>
