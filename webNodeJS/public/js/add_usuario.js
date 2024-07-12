var apiEndpoint = localStorage.getItem('apiEndpoint');
const passwdEdited = true;

document.addEventListener('DOMContentLoaded', (event) => {
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
                userRolSelect.appendChild(optionElement);
            });
        } else {
            localStorage.setItem('check_token', false);
            console.log('Token not valid');
            window.location.href = '/login';
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
                userStateSelect.appendChild(optionElement);
            });
        } else {
            localStorage.setItem('check_token', false);
            console.log('Token not valid');
            window.location.href = '/login';
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
});

function validarCorreoElectronico(email) {
    // Expresión regular para validar el formato del correo electrónico
    var regex = /^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9]){1,}?$/;

    if (!regex.test(email)) {
        alert("El correo electrónico no es válido.");
        return false;
    }

    return true;
}

// Función para enviar los datos del usuario a /api/users/admin_user_create
function send_data_user() {
    var email = document.getElementById('userName').value;
    var nombre_user = document.getElementById('userRealName').value;
    var id_rol = document.getElementById('userRol').value;
    var id_estado = document.getElementById('userState').value;
    var bodyRequest

    // Validar que el correo electrónico sea válido
    if (!validarCorreoElectronico(email)) {
        return;
    }

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
            email: email,
            nombre_user: nombre_user,
            id_rol: id_rol,
            id_estado: id_estado,
            passwd: passwdData,
            token: localStorage.getItem('user_token')
        });
    } else {
        alert('Debe ingresar una contraseña');
        return;
    }

    fetch(apiEndpoint + '/api/users/admin_user_create', {
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
                console.log('Usuario creado');
                window.location.href = '/admin_usuarios';
            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
                window.location.href = '/login';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Mostrar mensaje de error
            alert('Error al editar el producto');
            return;
        });

}