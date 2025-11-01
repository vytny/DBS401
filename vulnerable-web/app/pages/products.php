<?php
// Get all products
$result = executeQuery("SELECT * FROM products ORDER BY id ASC");
?>

<div class="products-container">
    <h2>Our Products</h2>

    <div class="products-grid">
        <?php if ($result && $result->num_rows > 0): ?>
            <?php while($product = $result->fetch_assoc()): ?>
                <div class="product-card">
                    <div class="product-image">
                        <span class="product-icon"><?php
                            $icons = ['💻', '🖱️', '⌨️', '🖥️', '🎧'];
                            echo $icons[$product['id'] % count($icons)];
                        ?></span>
                    </div>
                    <div class="product-info">
                        <h3><?php echo htmlspecialchars($product['name']); ?></h3>
                        <p class="product-description">
                            <?php echo htmlspecialchars(substr($product['description'], 0, 100)); ?>
                        </p>
                        <div class="product-price">$<?php echo number_format($product['price'], 2); ?></div>
                        <div class="product-stock">
                            <?php if ($product['stock'] > 0): ?>
                                <span class="in-stock">✓ In Stock (<?php echo $product['stock']; ?>)</span>
                            <?php else: ?>
                                <span class="out-of-stock">✗ Out of Stock</span>
                            <?php endif; ?>
                        </div>
                        <a href="index.php?page=product_detail&id=<?php echo $product['id']; ?>" class="btn btn-primary">
                            View Details
                        </a>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else: ?>
            <p>No products found.</p>
        <?php endif; ?>
    </div>
</div>

<style>
.products-container {
    padding: 20px;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    margin-top: 30px;
}

.product-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.product-image {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40px;
    text-align: center;
}

.product-icon {
    font-size: 64px;
}

.product-info {
    padding: 20px;
}

.product-info h3 {
    margin: 0 0 10px 0;
    font-size: 20px;
}

.product-description {
    color: #666;
    margin-bottom: 15px;
    min-height: 50px;
}

.product-price {
    font-size: 24px;
    font-weight: bold;
    color: #28a745;
    margin-bottom: 10px;
}

.product-stock {
    margin-bottom: 15px;
}

.in-stock {
    color: #28a745;
    font-weight: bold;
}

.out-of-stock {
    color: #dc3545;
    font-weight: bold;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 4px;
    text-align: center;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-primary:hover {
    background: #0056b3;
}
</style>
