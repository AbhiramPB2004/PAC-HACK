import React from 'react'
import "../CSS/ProductCreating.css"

function Product_Creating(){
    return(
    <div className="Product_Create">
        <header>
                <nav className='navhome'>
                    <a href="/">Home</a>
                    <div className="dropdown">
                        <a href="#">Products</a>
                        <div className="dropdown-content">
                            <a href="#">Vegetables</a>
                            <a href="#">Fruits</a>
                            <a href="#">Seeds</a>
                        </div>
                    </div>
                    <a href="#">Offers</a>
                    <a href="#">Contact</a>
                    <a href="/register">Register</a>
                    <a href="/login">Login</a>
                </nav>
            </header>
    
        <form className="Form_Class" action="/submit-product" method="POST" enctype="multipart/form-data">
         <h2>Create Your Product</h2>
            <div class="form-group">
                <label for="product-image">Product Image:</label>
                <input type="file" id="product-image" name="product-image" accept="image/*" required/>
            </div>

            <div class="form-group">
                <label for="product-name">Product Name:</label>
                <input type="text" id="product-name" name="product-name" placeholder="Enter product name" required/>
            </div>

            <div class="form-group">
                <label for="product-description">Product Description:</label>
                <textarea id="product-description" name="product-description" placeholder="Enter product description" required></textarea>
            </div>

            <div class="form-group">
                <label for="product-price">Price (in USD):</label>
                <input type="number" id="product-price" name="product-price" min="0" step="0.01" placeholder="Enter price" required/>
            </div>

            <div class="form-group">
                <label for="stock-quantity">Stock Quantity:</label>
                <input type="number" id="stock-quantity" name="stock-quantity" min="0" placeholder="Enter stock quantity" required/>
            </div>

            <button type="submit" class="submit-btn">Create Product</button>
        </form>
        <footer className="footer">
                <p>&copy; 2024 KISANET. All rights reserved.</p>
                <p>
                    <a href="#">Privacy Policy</a> | 
                    <a href="#">Terms of Service</a> | 
                    <a href="#">Contact Us</a>
                </p>
        </footer>
    </div>
)
};
export default Product_Creating