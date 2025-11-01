<?php
session_start();
require_once 'config.php';
require_once 'db.php';

$page = isset($_GET['page']) ? $_GET['page'] : 'home';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureShop - Online Store</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>🛒 SecureShop</h1>
            <nav>
                <a href="index.php?page=home">Home</a>
                <a href="index.php?page=products">Products</a>
                <a href="index.php?page=search">Search</a>
                <?php if (isset($_SESSION['user_id'])): ?>
                    <a href="index.php?page=profile">Profile</a>
                    <a href="logout.php">Logout (<?php echo htmlspecialchars($_SESSION['username']); ?>)</a>
                <?php else: ?>
                    <a href="index.php?page=login">Login</a>
                <?php endif; ?>
            </nav>
        </div>
    </header>

    <main class="container">
        <?php
        // Route to different pages (vulnerable to file inclusion)
        switch($page) {
            case 'home':
                include 'pages/home.php';
                break;
            case 'products':
                include 'pages/products.php';
                break;
            case 'product_detail':
                include 'pages/product_detail.php';
                break;
            case 'search':
                include 'pages/search.php';
                break;
            case 'login':
                include 'pages/login.php';
                break;
            case 'profile':
                include 'pages/profile.php';
                break;
            case 'admin':
                include 'pages/admin.php';
                break;
            default:
                echo "<h2>Page not found</h2>";
        }
        ?>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 SecureShop - Database Security CTF Lab</p>
            <p><small>Server: <?php echo $_SERVER['SERVER_SOFTWARE']; ?> | PHP: <?php echo phpversion(); ?></small></p>
        </div>
    </footer>
</body>
</html>
