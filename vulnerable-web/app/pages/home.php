<div class="home-container">
    <div class="hero">
        <h1>Welcome to SecureShop!</h1>
        <p>Your one-stop shop for all things tech</p>
        <a href="index.php?page=products" class="btn btn-primary btn-large">Browse Products</a>
    </div>

    <div class="features">
        <div class="feature-box">
            <h3>🔒 Secure Payments</h3>
            <p>Your transactions are safe with our advanced security measures</p>
        </div>
        <div class="feature-box">
            <h3>🚚 Fast Shipping</h3>
            <p>Get your products delivered quickly to your doorstep</p>
        </div>
        <div class="feature-box">
            <h3>💯 Quality Products</h3>
            <p>Only the best products from trusted manufacturers</p>
        </div>
    </div>

    <div class="info-box">
        <h3>About This Application</h3>
        <p>This is a demonstration e-commerce application built for educational purposes.</p>
        <p><strong>Server Information:</strong></p>
        <ul>
            <li>Web Server: <?php echo $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown'; ?></li>
            <li>PHP Version: <?php echo phpversion(); ?></li>
            <li>Database: MySQL <?php
                $version = executeQuery("SELECT VERSION() as version");
                if ($version) {
                    $row = $version->fetch_assoc();
                    echo $row['version'];
                }
            ?></li>
        </ul>
    </div>
</div>

<style>
.home-container {
    padding: 20px;
}

.hero {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 40px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 20px;
}

.hero p {
    font-size: 20px;
    margin-bottom: 30px;
}

.btn-large {
    padding: 15px 40px;
    font-size: 18px;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}

.feature-box {
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.feature-box h3 {
    font-size: 24px;
    margin-bottom: 15px;
}

.info-box {
    background: #f8f9fa;
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid #007bff;
}

.info-box ul {
    list-style: none;
    padding-left: 0;
}

.info-box li {
    padding: 5px 0;
}
</style>
