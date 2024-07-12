var apiEndpoint = localStorage.getItem('apiEndpoint');

// Check if user is logged in
document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/users/user_refresh_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: localStorage.getItem('user_token') }),
    })
        .then(response => response.json())
        .then(data => {
            var loginIndicator = document.getElementById('loginIndicator');
            var logoutItem = document.getElementById('logoutItem');
            if (data.check_token === true) {
                // Cambiar el texto del indicador de login al correo del usuario
                loginIndicator.textContent = localStorage.getItem('username');
                // Eliminar el comportamiento de redirección del indicador de login
                loginIndicator.href = '/user_manager?user=' + localStorage.getItem('username');
                localStorage.setItem('check_token', 'true');

                // Agregar el botón de logout al navbar
                logoutItem.textContent = 'Logout';
            } else if (data.check_token === false) {
                // Cambiar el texto del indicador de login a 'Login'
                loginIndicator.textContent = 'Login';
                // Cambiar la ruta del indicador de login a la página de login
                loginIndicator.href = '/login';
                localStorage.setItem('check_token', 'false');

                // Eliminar el botón de logout del navbar
                logoutItem.textContent = '';
            }
        })
        .catch((error) => {
            console.error('Error General1:', error);
        });
});

// Validar si el usuario es Administrador
document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/users/admin_validate_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: localStorage.getItem('user_token') }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                // Agregar las vistas de administrador al navbar
                var views = document.getElementById('pagesItems');
                var adminViews = document.createElement('li');
                adminViews.classList.add('nav-item');
                adminViews.innerHTML = `
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Panel Administrativo
                  </a>
                  <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <a class="dropdown-item" href="admin_productos">Productos</a>
                    <a class="dropdown-item" href="admin_pedidos">Pedidos</a>
                    <a class="dropdown-item" href="admin_usuarios">Usuarios</a>
                  </div>
                `;
                views.appendChild(adminViews);
                
            } else if (data.check_token === false) {
                localStorage.setItem('is_admin', 'false');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

// Add Economic indicator to localstorage

fetch('https://mindicador.cl/api').then(function(response) {
    return response.json();
}).then(function(dailyIndicators) {
    localStorage.setItem('usdvalue', dailyIndicators.dolar.valor);
}).catch(function(error) {
    console.log('Requestfailed', error);
});

// Validar si el usuario está autenticado
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        if (localStorage.getItem('check_token') !== 'true' && window.location.pathname !== '/login') {
            // Redirigir a la página de login
            window.location.href = '/login';
        }
    }, 1000)
});

// Obtener el carrito del usuario
document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/pedidos/load_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token: localStorage.getItem('user_token'),
            mailUser: localStorage.getItem('username')
        }),
    })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('idPedido', 'undefined');
            localStorage.setItem('idPedido', data.order.idPedido);
        })
        .catch((error) => {
            localStorage.setItem('idPedido', 'undefined');
            console.error('Error:', error);
        });
});

// Logica Logout
function logout() {
    localStorage.clear();
    window.location.href = '/';
}