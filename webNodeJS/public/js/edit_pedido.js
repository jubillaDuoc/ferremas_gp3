var apiEndpoint = localStorage.getItem('apiEndpoint');
var urlParams = new URLSearchParams(window.location.search);
var idPedido = urlParams.get('idPedido');
var order = null;
var orderLoaded = false;

document.addEventListener('DOMContentLoaded', (event) => {
    // Cargar detalle del pedido

    fetch(apiEndpoint + '/api/pedidos/get_order_fulldetail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            idOrder: idPedido,
            token: localStorage.getItem('user_token')
        }),
    })
    .then(response => response.json()).then(data => {
        if (data.check_token === true) {
            localStorage.setItem('check_token', true);

            order = data.order;

            console.log('idProducto ' + data.order.id_pedido);

            element = document.getElementById('idPedido')
            element.textContent = order.id_pedido;

            element = document.getElementById('userMail')
            element.textContent = order.email_user;

            element = document.getElementById('userName')
            element.textContent = order.nombre_user;

            element = document.getElementById('userRol')
            element.textContent = order.nombre_user_rol;

            element = document.getElementById('userState')
            element.textContent = order.nombre_user_state;

            element = document.getElementById('totalPedido')
            element.textContent = order.total_pedido;

            fetch(apiEndpoint + '/api/pedidos/get_order_states', {
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

                    var estadoSelect = document.getElementById('nombreEstadoPedido');
                    estadoSelect.innerHTML = '';

                    states.forEach(state => {
                        var optionElement = document.createElement('option');
                        optionElement.value = state.id_estado_pedido;
                        optionElement.textContent = state.nombre_estado_pedido;
                        if (state.id_estado_pedido === order.id_estado_pedido) {
                            optionElement.selected = true;
                        }
                        estadoSelect.appendChild(optionElement);
                    });
                } else {
                    localStorage.setItem('check_token', false);
                    console.log('Token not valid');
                }
            }).catch((error) => {
                console.error('Error:', error);
            });

            orderLoaded = true;
            
            // Cargar productos del pedido
            var tableBody = document.getElementById('productos-tabla');

            order.productos.forEach(producto => {
                var row = document.createElement('tr');

                    var nombreProductoCell = document.createElement('td');
                    var link = document.createElement('a');
                    link.textContent = producto.nombre_producto;
                    link.href = '/detalle_producto?idProducto=' + producto.id_producto;
                    nombreProductoCell.appendChild(link);
                    row.appendChild(nombreProductoCell);

                    var cantidadCell = document.createElement('td');
                    cantidadCell.textContent = producto.cantidad_producto;
                    row.appendChild(cantidadCell);

                    var precioCell = document.createElement('td');
                    precioCell.textContent = producto.precio_producto;
                    row.appendChild(precioCell);

                    var accionesCell = document.createElement('td');
                    var eliminarButton = document.createElement('button');
                    eliminarButton.textContent = 'Eliminar';
                    eliminarButton.addEventListener('click', function() {
                        var idProducto = producto.id_producto;
                        
                        fetch(apiEndpoint + '/api/pedidos/remove_product_from_order', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                idOrder: order.id_pedido,
                                idProducto: idProducto,
                                token: localStorage.getItem('user_token')
                            }),
                        })
                            .then(response => response.json())
                            .then(data => {
                                window.location.reload();
                            })
                            .catch((error) => {
                                console.error('Error:', error);
                            });
                    });
                    accionesCell.appendChild(eliminarButton);
                    row.appendChild(accionesCell);

                    tableBody.appendChild(row);
            });

        } else {
            localStorage.setItem('check_token', false);
            console.log('Token not valid');
            orderLoaded = false;
            window.location.reload();
        }
    }).catch((error) => {
        console.error('Error:', error);
        orderLoaded = false;
    });
});

// Función para enviar los datos del producto a /api/pedidos/update_order_status
function save_newState() {
    var id_estado_pedido = document.getElementById('nombreEstadoPedido').value;

    if (orderLoaded === true){
        fetch(apiEndpoint + '/api/pedidos/update_order_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                status_id: id_estado_pedido,
                idOrder: order.id_pedido,
                token: localStorage.getItem('user_token')
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.check_token === true) {
                    localStorage.setItem('check_token', true);
                    console.log('Producto editado');
                    window.location.reload();
                } else {
                    localStorage.setItem('check_token', false);
                    console.log('Token not valid');
                    window.location.reload();
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                // Mostrar mensaje de error
                alert('Error al editar el producto');
                return;
            });
    } else {
        window.location.reload();
    }
}

// Logica boton Recargar Carrito
function reloadPedido() {
    window.location.reload();
}

// Logica boton Vaciar Carrito
function vaciarCarritoBoton() {
    var idPedido = localStorage.getItem('idPedido');
    fetch(apiEndpoint + '/api/pedidos/clear_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            idPedido: idPedido,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}