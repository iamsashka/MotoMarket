document.addEventListener('DOMContentLoaded', function() {
    // ========== Фильтрация ==========
    const categorySelect = document.getElementById('category');
    const tagSelect = document.getElementById('tags');
    const priceSelect = document.getElementById('price');
    const resetBtn = document.getElementById('resetFilters');
    
    // Обработчик фильтрации по категориям
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const value = this.value;
            if (value === 'all') {
                window.location.href = '/catalog/';
            } else {
                window.location.href = `/catalog/category/${value}/`;
            }
        });
    }
    
    // Обработчик фильтрации по тегам
    if (tagSelect) {
        tagSelect.addEventListener('change', function() {
            const value = this.value;
            if (value === 'all') {
                window.location.href = '/catalog/';
            } else {
                window.location.href = `/catalog/tags/${value}/`;
            }
        });
    }
    
    // Обработчик фильтрации по цене (примерная реализация)
    if (priceSelect) {
        priceSelect.addEventListener('change', function() {
            const value = this.value;
            const url = new URL(window.location.href);
            
            if (value === 'all') {
                url.searchParams.delete('price');
            } else {
                url.searchParams.set('price', value);
            }
            
            window.location.href = url.toString();
        });
    }
    
    // Обработчик сброса фильтров
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            window.location.href = '/catalog/';
        });
    }

    // ========== Корзина ==========
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const button = this.querySelector('button[type="submit"]');
            
            if (!button) return;
            
            const originalHtml = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Добавляем...';
            
            try {
                const formData = new FormData(this);
                const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
                
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    }
                });
                
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                
                const data = await response.json();
                
                if (data.success) {
                    // Обновляем счетчик корзины
                    updateCartCounter(data.cart_items_count || 0);
                    
                    // Показываем анимацию
                    showAddAnimation(button);
                } else {
                    throw new Error(data.message || 'Ошибка добавления в корзину');
                }
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            } finally {
                button.disabled = false;
                button.innerHTML = originalHtml;
            }
        });
    });
    
    function updateCartCounter(count) {
        const counters = document.querySelectorAll('.cart-count');
        counters.forEach(counter => {
            counter.textContent = count > 0 ? `(${count})` : '';
        });
    }
    
    function showAddAnimation(button) {
        const anim = document.createElement('span');
        anim.className = 'add-animation';
        anim.textContent = '+1';
        button.appendChild(anim);
        
        setTimeout(() => {
            anim.remove();
        }, 1000);
    }
});