// Cart functionality
let cart = JSON.parse(localStorage.getItem('annadata_cart')) || [];

function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(el => {
        el.textContent = totalItems;
    });
}

function addToCart(productId, name, price, weight, image) {
    const existingItem = cart.find(item => item.id === productId && item.weight === weight);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name,
            price,
            weight,
            image,
            quantity: 1
        });
    }
    
    localStorage.setItem('annadata_cart', JSON.stringify(cart));
    updateCartCount();
    showNotification('Product added to cart!');
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--primary-green);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

// Weight selector functionality
function setupWeightSelectors() {
    const weightOptions = document.querySelectorAll('.weight-option');
    weightOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            weightOptions.forEach(opt => opt.classList.remove('active'));
            // Add active class to clicked option
            this.classList.add('active');
            
            // Update price based on weight
            const basePrice = parseFloat(this.dataset.basePrice);
            const multiplier = parseFloat(this.dataset.multiplier);
            const newPrice = basePrice * multiplier;
            
            const priceElement = this.closest('.product-detail-container').querySelector('.product-price');
            if (priceElement) {
                priceElement.textContent = `₹${newPrice.toFixed(2)}`;
            }
        });
    });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#dc3545';
            } else {
                input.style.borderColor = '#e0e0e0';
            }
        });
        
        if (isValid) {
            showNotification('Form submitted successfully!');
            form.reset();
        } else {
            showNotification('Please fill in all required fields!');
        }
    });
}

// Initialize functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart count
    updateCartCount();
    
    // Setup weight selectors on product detail page
    setupWeightSelectors();
    
    // Setup form validation
    validateForm('farmerRegistrationForm');
    validateForm('contactForm');
    
    // Add to cart buttons functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart') || 
            e.target.closest('.add-to-cart')) {
            const button = e.target.classList.contains('add-to-cart') ? 
                          e.target : e.target.closest('.add-to-cart');
            
            const productCard = button.closest('.product-card');
            if (productCard) {
                const productId = productCard.dataset.id;
                const productName = productCard.dataset.name;
                const productPrice = parseFloat(productCard.dataset.price);
                const productImage = productCard.dataset.image;
                const selectedWeight = productCard.querySelector('.weight-selector')?.value || '500gm';
                
                addToCart(productId, productName, productPrice, selectedWeight, productImage);
            }
        }
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});