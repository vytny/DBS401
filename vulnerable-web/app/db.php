<?php
// Database Connection

function getDBConnection() {
    static $conn = null;

    if ($conn === null) {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $conn->set_charset("utf8mb4");
    }

    return $conn;
}

// Get connection
$conn = getDBConnection();

// Helper function for vulnerable queries (NO INPUT SANITIZATION)
function executeQuery($sql) {
    global $conn;

    if (DEBUG_MODE) {
        // Intentionally show query for debugging (information disclosure)
        echo "<!-- DEBUG: SQL Query: " . htmlspecialchars($sql) . " -->\n";
    }

    $result = $conn->query($sql);

    if (!$result && DEBUG_MODE) {
        echo "<!-- DEBUG: SQL Error: " . htmlspecialchars($conn->error) . " -->\n";
    }

    return $result;
}

// Vulnerable function - direct string concatenation
function getUserByCredentials($username, $password) {
    global $conn;

    // VULNERABILITY: SQL Injection - no parameterization
    $sql = "SELECT * FROM users WHERE username = '$username' AND password = MD5('$password')";

    if (DEBUG_MODE) {
        echo "<!-- DEBUG: Login Query: " . htmlspecialchars($sql) . " -->\n";
    }

    $result = $conn->query($sql);

    if ($result && $result->num_rows > 0) {
        return $result->fetch_assoc();
    }

    return false;
}

// Vulnerable search function
function searchProducts($search_term) {
    global $conn;

    // VULNERABILITY: SQL Injection in LIKE clause
    $sql = "SELECT * FROM products WHERE name LIKE '%$search_term%' OR description LIKE '%$search_term%'";

    return executeQuery($sql);
}

// Vulnerable product detail function
function getProductById($id) {
    global $conn;

    // VULNERABILITY: SQL Injection - numeric parameter not validated
    $sql = "SELECT * FROM products WHERE id = $id";

    return executeQuery($sql);
}

// Vulnerable admin check
function checkAdminCredentials($username, $password) {
    global $conn;

    // VULNERABILITY: SQL Injection in admin authentication
    $sql = "SELECT * FROM admin_panel WHERE username = '$username' AND password = '$password'";

    if (DEBUG_MODE) {
        echo "<!-- DEBUG: Admin Query: " . htmlspecialchars($sql) . " -->\n";
    }

    $result = $conn->query($sql);

    if ($result && $result->num_rows > 0) {
        return $result->fetch_assoc();
    }

    return false;
}

// Function to get user by ID (also vulnerable)
function getUserById($user_id) {
    global $conn;

    $sql = "SELECT * FROM users WHERE id = $user_id";
    $result = executeQuery($sql);

    if ($result && $result->num_rows > 0) {
        return $result->fetch_assoc();
    }

    return false;
}

// Function to log user action (for trigger challenge)
function logUserAction($user_id, $action, $ip_address) {
    global $conn;

    $sql = "INSERT INTO user_logs (user_id, action, ip_address) VALUES ($user_id, '$action', '$ip_address')";
    return executeQuery($sql);
}
?>
