document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.add-to-cart-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const button = this.querySelector('.add-to-cart-btn');
            
            // Показываем анимацию загрузки
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Добавляем...';
            
            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: new FormData(this),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
                    }
                });
                if (response.redirected) {
                    window.location.href = response.url;  
                    return;
                }
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.message || 'Ошибка сервера');
                }
                
                if (data.success) {
                    // Обновляем счетчик корзины
                    const cartCounters = document.querySelectorAll('.cart-count');
                    cartCounters.forEach(counter => {
                        counter.textContent = data.cart_length > 0 ? `(${data.cart_length})` : '';
                    });
                    
                    // Показываем анимацию "+1"
                    showAddToCartAnimation(button);
                    
                    // Показываем уведомление
                    showNotification(data.message);
                } else {
                    showNotification(data.message || 'Ошибка добавления', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification(error.message || 'Ошибка при добавлении в корзину', 'error');
            } finally {
                // Восстанавливаем кнопку
                button.disabled = false;
                button.innerHTML = '<i class="fas fa-shopping-cart"></i> В корзину';
            }
        });
    });
    
    function showAddToCartAnimation(button) {
        const animation = document.createElement('div');
        animation.className = 'add-to-cart-animation';
        animation.textContent = '+1';
        
        const rect = button.getBoundingClientRect();
        animation.style.left = `${rect.left + rect.width/2 - 10}px`;
        animation.style.top = `${rect.top}px`;
        
        document.body.appendChild(animation);
        
        setTimeout(() => {
            animation.remove();
        }, 1000);
    }
    
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }
});


function filterByCategory() {
    const categoryId = document.getElementById('category').value;
    if (categoryId === 'all') {
        window.location.href = "{% url 'firstpractooos:catalog' %}";
    } else {
        window.location.href = "{% url 'firstpractooos:catalog_by_category' 0 %}".replace('0', categoryId);
    }
}