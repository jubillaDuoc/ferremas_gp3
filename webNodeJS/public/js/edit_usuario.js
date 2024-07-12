var apiEndpoint = localStorage.getItem('apiEndpoint');
var urlParams = new URLSearchParams(window.location.search);
var idUser = urlParams.get('idUser');
passwdEdited = false;

document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/users/get_user_by_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_user: idUser,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);

                var user = data.user;

                console.log('idUser ' + data.user.idUser);

                element = document.getElementById('idUser')
                element.textContent = user.id_user;

                element = document.getElementById('userName')
                element.value = user.email_user;

                element = document.getElementById('userRealName')
                element.value = user.nombre_user;

                fetch(apiEndpoint + '/api/users/get_roles', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token: localStorage.getItem('user_token')
                    }),
                }).then(response => response.json()).then(data => {
                    if (data.check_token === true) {
                        localStorage.setItem('check_token', true);

                        var roles = data.roles;

                        var userRolSelect = document.getElementById('userRol');
                        userRolSelect.innerHTML = '';

                        roles.forEach(rol => {
                            var optionElement = document.createElement('option');
                            optionElement.value = rol.id_user_rol;
                            optionElement.textContent = rol.nombre_user_rol;
                            if (rol.id_user_rol === user.id_user_rol) {
                                optionElement.selected = true;
                            }
                            userRolSelect.appendChild(optionElement);
                        });
                    } else {
                        localStorage.setItem('check_token', false);
                        console.log('Token not valid');
                    }
                }).catch((error) => {
                    console.error('Error:', error);
                });

                fetch(apiEndpoint + '/api/users/get_states', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token: localStorage.getItem('user_token')
                    }),
                }).then(response => response.json()).then(data => {
                    if (data.check_token === true) {
                        localStorage.setItem('check_token', true);

                        var states = data.states;

                        var userStateSelect = document.getElementById('userState');
                        userStateSelect.innerHTML = '';

                        states.forEach(state => {
                            var optionElement = document.createElement('option');
                            optionElement.value = state.id_user_state;
                            optionElement.textContent = state.nombre_user_state;
                            if (state.id_user_state === user.id_user_state) {
                                optionElement.selected = true;
                            }
                            userStateSelect.appendChild(optionElement);
                        });
                    } else {
                        localStorage.setItem('check_token', false);
                        console.log('Token not valid');
                    }
                }).catch((error) => {
                    console.error('Error:', error);
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

// Función para validar checkbox de contraseña
function checkEditPass() {
    var editPass = document.getElementById('editPass');
    var firstNewPasswd = document.getElementById('firstNewPasswd');
    var secondNewPasswd = document.getElementById('secondNewPasswd');
    if (editPass.checked) {
        // Quitar readonly
        firstNewPasswd.disabled = false;
        secondNewPasswd.disabled = false;
        passwdEdited = true;
    } else {
        firstNewPasswd.disabled = true;
        secondNewPasswd.disabled = true;
        passwdEdited = false;
    }
}

// Función para enviar los datos del usuario a /api/users/user_update_admin
function send_data_user() {
    var idUser = document.getElementById('idUser').textContent;
    var nombre_user = document.getElementById('userRealName').value;
    var id_rol = document.getElementById('userRol').value;
    var id_estado = document.getElementById('userState').value;
    var bodyRequest

    if (passwdEdited === true) {
        var passwd = document.getElementById('firstNewPasswd').value;
        var passwd2 = document.getElementById('secondNewPasswd').value;
        if (passwd !== passwd2) {
            alert('Las contraseñas no coinciden');
            return;
        }
        // Validar que la passwd sean solo caracteres alfanumericos
        if (!/^[a-zA-Z0-9]*$/.test(passwd)) {
            alert('La contraseña solo puede contener letras y números');
            return;
        } else {
            var passwdData = passwd;
        }
        bodyRequest = JSON.stringify({
            idUser: idUser,
            nombre_user: nombre_user,
            id_rol: id_rol,
            id_estado: id_estado,
            passwd: passwdData,
            token: localStorage.getItem('user_token')
        });
    } else {
        bodyRequest = JSON.stringify({
            idUser: idUser,
            nombre_user: nombre_user,
            id_rol: id_rol,
            id_estado: id_estado,
            token: localStorage.getItem('user_token')
        });
    }

    fetch(apiEndpoint + '/api/users/user_update_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: bodyRequest,
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);
                console.log('Usuario editado');
                window.location.href = '/admin_usuarios';
            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
                window.location.reload()
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Mostrar mensaje de error
            alert('Error al editar el producto');
            return;
        });

}