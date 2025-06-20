document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    
    menuToggle.addEventListener('click', function() {
        nav.classList.toggle('active');
        this.classList.toggle('active');
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add to cart functionality
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const bikeId = this.getAttribute('data-id');
            
            // Animation
            this.innerHTML = '<i class="fas fa-check"></i> Добавлено';
            this.classList.add('added');
            
            setTimeout(() => {
                this.innerHTML = 'В корзину';
                this.classList.remove('added');
            }, 2000);
            
            // Update cart count
            updateCartCount(1);
        });
    });

    // Hero slider
    const heroSlider = document.querySelector('.hero__slider');
    if (heroSlider) {
        // In a real project you would implement a proper slider here
        // For demo we'll just add a simple animation
        setInterval(() => {
            heroSlider.style.backgroundPosition = 'center ' + (Math.random() * 20 - 10) + 'px';
        }, 5000);
    }

    // Intersection Observer for scroll animations
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.slide-up, .fade-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(element => {
            observer.observe(element);
        });
    };

    animateOnScroll();
});

function updateCartCount(quantity) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const currentCount = parseInt(cartCount.textContent) || 0;
        cartCount.textContent = currentCount + quantity;
        
        // Animation
        cartCount.classList.add('updated');
        setTimeout(() => {
            cartCount.classList.remove('updated');
        }, 300);
    }
}