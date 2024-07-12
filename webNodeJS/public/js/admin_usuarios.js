var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {

    fetch(apiEndpoint + '/api/users/user_get_all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);
                var tableBody = document.getElementById('resultado-tabla');

                data.users.forEach(user => {
                    var row = document.createElement('tr');

                    var idCell = document.createElement('td');
                    idCell.textContent = user.id_user;
                    row.appendChild(idCell);

                    var userCell = document.createElement('td');
                    var link = document.createElement('a');
                    link.textContent = user.email_user;
                    link.href = '/edit_usuario?idUser=' + user.id_user;
                    userCell.appendChild(link);
                    row.appendChild(userCell);

                    var nombreCell = document.createElement('td');
                    nombreCell.textContent = user.nombre_user;
                    row.appendChild(nombreCell);
                    
                    var userRolCell = document.createElement('td');
                    userRolCell.textContent = user.nombre_user_rol;
                    row.appendChild(userRolCell);

                    var userStateCell = document.createElement('td');
                    userStateCell.textContent = user.nombre_user_state;
                    row.appendChild(userStateCell);


                    // Editar User
                    var accionesCell = document.createElement('td');
                    var agregarButton = document.createElement('button');
                    agregarButton.textContent = 'Modificar';
                    agregarButton.classList.add('btn', 'btn-secondary');
                    agregarButton.addEventListener('click', () => {
                        window.location.href = '/edit_usuario?idUser=' + user.id_user;
                    });
                    accionesCell.appendChild(agregarButton);
                    row.appendChild(accionesCell);

                    tableBody.appendChild(row);
                });
            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
                window.location.href = '/login';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});