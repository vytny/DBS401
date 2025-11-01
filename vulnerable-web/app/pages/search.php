<?php
$search_term = '';
$results = null;

if (isset($_GET['q'])) {
    $search_term = $_GET['q'];

    // VULNERABILITY: SQL Injection in search
    $results = searchProducts($search_term);
}
?>

<div class="search-container">
    <h2>Search Products</h2>

    <form method="GET" action="" class="search-form">
        <input type="hidden" name="page" value="search">
        <div class="search-box">
            <input type="text"
                   name="q"
                   value="<?php echo htmlspecialchars($search_term); ?>"
                   placeholder="Search for products..."
                   class="search-input">
            <button type="submit" class="btn btn-primary">Search</button>
        </div>
    </form>

    <?php if ($search_term !== ''): ?>
        <div class="search-results">
            <h3>Search Results for: "<?php echo htmlspecialchars($search_term); ?>"</h3>

            <?php if ($results && $results->num_rows > 0): ?>
                <p class="results-count">Found <?php echo $results->num_rows; ?> product(s)</p>

                <div class="products-list">
                    <?php while($product = $results->fetch_assoc()): ?>
                        <div class="product-item">
                            <div class="product-icon-small">
                                <?php
                                $icons = ['💻', '🖱️', '⌨️', '🖥️', '🎧'];
                                echo $icons[$product['id'] % count($icons)];
                                ?>
                            </div>
                            <div class="product-details">
                                <h4><?php echo htmlspecialchars($product['name']); ?></h4>
                                <p><?php echo htmlspecialchars($product['description']); ?></p>
                                <div class="product-price-small">$<?php echo number_format($product['price'], 2); ?></div>
                            </div>
                            <div class="product-actions">
                                <a href="index.php?page=product_detail&id=<?php echo $product['id']; ?>" class="btn btn-primary">
                                    View Details
                                </a>
                            </div>
                        </div>
                    <?php endwhile; ?>
                </div>
            <?php else: ?>
                <div class="no-results">
                    <p>No products found matching your search.</p>
                    <p>Try different keywords or browse all products.</p>
                </div>
            <?php endif; ?>
        </div>
    <?php else: ?>
        <div class="search-hints">
            <h3>Search Tips:</h3>
            <ul>
                <li>Try searching for: laptop, mouse, keyboard, monitor, headphones</li>
                <li>Use specific product names for better results</li>
                <li>Search terms are case-insensitive</li>
            </ul>

            <div class="sql-hint">
                <h4>🔍 Advanced Search</h4>
                <p>This search uses SQL LIKE queries. Try testing different patterns!</p>
                <code>Example: laptop OR 1=1 --</code>
            </div>
        </div>
    <?php endif; ?>
</div>

<style>
.search-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.search-form {
    margin: 30px 0;
}

.search-box {
    display: flex;
    gap: 10px;
}

.search-input {
    flex: 1;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.search-input:focus {
    outline: none;
    border-color: #007bff;
}

.search-results {
    margin-top: 30px;
}

.results-count {
    color: #666;
    margin-bottom: 20px;
}

.products-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.product-item {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.product-icon-small {
    font-size: 48px;
    min-width: 80px;
    text-align: center;
}

.product-details {
    flex: 1;
}

.product-details h4 {
    margin: 0 0 10px 0;
    font-size: 20px;
}

.product-details p {
    color: #666;
    margin-bottom: 10px;
}

.product-price-small {
    font-size: 20px;
    font-weight: bold;
    color: #28a745;
}

.product-actions {
    min-width: 150px;
}

.no-results {
    text-align: center;
    padding: 60px 20px;
    background: white;
    border-radius: 8px;
}

.search-hints {
    margin-top: 40px;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.search-hints ul {
    margin: 15px 0;
    padding-left: 20px;
}

.search-hints li {
    margin: 8px 0;
}

.sql-hint {
    margin-top: 25px;
    padding: 20px;
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    border-radius: 4px;
}

.sql-hint h4 {
    margin: 0 0 10px 0;
}

.sql-hint code {
    display: block;
    margin-top: 10px;
    padding: 10px;
    background: #fff;
    border-radius: 4px;
    font-family: monospace;
}
</style>
