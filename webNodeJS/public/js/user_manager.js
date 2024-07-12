var apiEndpoint = localStorage.getItem('apiEndpoint');
var urlParams = new URLSearchParams(window.location.search);
var mail_user = urlParams.get('user');
passwdEdited = false;
var user

document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/users/get_user_by_mail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mail_user: mail_user,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);

                user = data.user;

                console.log('idUser ' + data.user.idUser);

                element = document.getElementById('idUser')
                element.textContent = user.id_user;

                element = document.getElementById('userName')
                element.value = user.email_user;

                element = document.getElementById('userRealName')
                element.value = user.nombre_user;

                element = document.getElementById('userRol')
                element.value = user.nombre_user_rol;

                element = document.getElementById('userState')
                element.value = user.nombre_user_state;
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
    var idUser = user.id_user;
    var nombre_user = document.getElementById('userRealName').value;
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
            passwd: passwdData,
            token: localStorage.getItem('user_token')
        });
        // Alertar al usuario de que se cerrará su sesion, abortar en caso de negativa del usuario
        if (confirm('Atencion, Se cerrará su sesión, por favor confirme accion')) {
            console.log('Cambio pass auth')
        } else {
            return;
        }
    } else {
        bodyRequest = JSON.stringify({
            idUser: idUser,
            nombre_user: nombre_user,
            token: localStorage.getItem('user_token')
        });
    }

    fetch(apiEndpoint + '/api/users/user_update', {
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
                window.location.reload();
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