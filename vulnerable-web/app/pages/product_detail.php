<?php
// VULNERABILITY: SQL Injection - ID parameter not sanitized
$product_id = $_GET['id'] ?? 1;

$result = getProductById($product_id);

if ($result && $result->num_rows > 0) {
    $product = $result->fetch_assoc();
} else {
    echo "<div class='alert alert-error'>Product not found!</div>";
    return;
}

// Get comments for this product
$comments_result = executeQuery("SELECT c.*, u.username FROM comments c JOIN users u ON c.user_id = u.id WHERE c.product_id = $product_id ORDER BY c.created_at DESC");
?>

<div class="product-detail-container">
    <div class="product-detail">
        <div class="product-image-large">
            <span class="product-icon-large"><?php
                $icons = ['💻', '🖱️', '⌨️', '🖥️', '🎧'];
                echo $icons[$product['id'] % count($icons)];
            ?></span>
        </div>

        <div class="product-info-detail">
            <h1><?php echo htmlspecialchars($product['name']); ?></h1>

            <div class="product-meta">
                <span class="category">Category: <?php echo htmlspecialchars($product['category']); ?></span>
                <span class="product-id">Product ID: <?php echo htmlspecialchars($product['id']); ?></span>
            </div>

            <div class="product-price-large">$<?php echo number_format($product['price'], 2); ?></div>

            <div class="product-stock-info">
                <?php if ($product['stock'] > 0): ?>
                    <span class="in-stock">✓ In Stock (<?php echo $product['stock']; ?> available)</span>
                <?php else: ?>
                    <span class="out-of-stock">✗ Out of Stock</span>
                <?php endif; ?>
            </div>

            <div class="product-description-full">
                <h3>Description</h3>
                <p><?php echo htmlspecialchars($product['description']); ?></p>
            </div>

            <?php if (isset($product['hidden_flag']) && !empty($product['hidden_flag'])): ?>
                <div class="hidden-data" style="display:none;">
                    <!-- Hidden Flag: <?php echo htmlspecialchars($product['hidden_flag']); ?> -->
                </div>
            <?php endif; ?>

            <button class="btn btn-primary btn-large">Add to Cart</button>
            <a href="index.php?page=products" class="btn btn-secondary">Back to Products</a>
        </div>
    </div>

    <div class="comments-section">
        <h2>Customer Reviews</h2>

        <?php if ($comments_result && $comments_result->num_rows > 0): ?>
            <?php while($comment = $comments_result->fetch_assoc()): ?>
                <div class="comment">
                    <div class="comment-header">
                        <strong><?php echo htmlspecialchars($comment['username']); ?></strong>
                        <span class="rating">
                            <?php for($i = 0; $i < $comment['rating']; $i++) echo '⭐'; ?>
                        </span>
                        <span class="comment-date"><?php echo date('M d, Y', strtotime($comment['created_at'])); ?></span>
                    </div>
                    <div class="comment-body">
                        <?php echo htmlspecialchars($comment['comment']); ?>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else: ?>
            <p>No reviews yet. Be the first to review this product!</p>
        <?php endif; ?>
    </div>
</div>

<style>
.product-detail-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.product-detail {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 40px;
    margin-bottom: 40px;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.product-image-large {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60px;
    text-align: center;
    border-radius: 8px;
}

.product-icon-large {
    font-size: 128px;
}

.product-info-detail h1 {
    margin: 0 0 20px 0;
    font-size: 32px;
}

.product-meta {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    color: #666;
}

.product-price-large {
    font-size: 36px;
    font-weight: bold;
    color: #28a745;
    margin-bottom: 15px;
}

.product-stock-info {
    margin-bottom: 20px;
    font-size: 18px;
}

.product-description-full {
    margin-bottom: 30px;
}

.product-description-full h3 {
    margin-bottom: 10px;
}

.btn-large {
    padding: 15px 30px;
    font-size: 18px;
    margin-right: 10px;
}

.btn-secondary {
    background: #6c757d;
    color: white;
    padding: 15px 30px;
    font-size: 18px;
    text-decoration: none;
    display: inline-block;
    border-radius: 4px;
}

.btn-secondary:hover {
    background: #545b62;
}

.comments-section {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.comment {
    border-bottom: 1px solid #eee;
    padding: 20px 0;
}

.comment:last-child {
    border-bottom: none;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
}

.comment-date {
    color: #999;
    font-size: 14px;
    margin-left: auto;
}

.comment-body {
    color: #333;
    line-height: 1.6;
}
</style>
