var apiEndpoint = localStorage.getItem('apiEndpoint');

document.getElementById('loginButton').addEventListener('click', function () {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch(apiEndpoint + '/api/users/user_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Guardar el token y el usuario en localStorage
            localStorage.setItem('user_token', data.token);
            localStorage.setItem('username', username);
            localStorage.setItem('check_token', true);
            // Redirigir al usuario a la página de inicio
            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});