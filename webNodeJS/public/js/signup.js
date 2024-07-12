var apiEndpoint = localStorage.getItem('apiEndpoint');
const passwdEdited = true;

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
            passwd: passwdData
        });
    } else {
        alert('Debe ingresar una contraseña');
        return;
    }

    fetch(apiEndpoint + '/api/users/user_create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: bodyRequest,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error === 'El usuario ya existe.') {
                alert('El usuario ya existe.');
                window.location.reload();
            } else {
                alert('Usuario creado');
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