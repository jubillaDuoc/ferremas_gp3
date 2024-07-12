var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {
    var USD = localStorage.getItem('usdvalue');

    fetch(apiEndpoint + '/api/pedidos/get_order_detail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token: localStorage.getItem('user_token'),
            idOrder: localStorage.getItem('idPedido')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);

                // Cargar datos del pedido
                var order = data.order;

                element = document.getElementById('idPedido')
                element.textContent = order.idPedido;

                element = document.getElementById('totalPedidoCLP')
                element.textContent = order.totalPedido;

                element = document.getElementById('totalPedidoUSD')
                element.textContent = (order.totalPedido / USD).toFixed(2);

                // Cargar productos del pedido
                var tableProducto = document.getElementById('producto-tabla');

                data.order.productos.forEach(producto => {
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

                    var precioCell = document.createElement('td');
                    precioCell.textContent = (producto.precio_producto / USD).toFixed(2);
                    row.appendChild(precioCell);

                    var accionesCell = document.createElement('td');
                    var eliminarButton = document.createElement('button');
                    eliminarButton.textContent = 'Eliminar';
                    eliminarButton.addEventListener('click', function() {
                        var idPedido = data.order.idPedido;
                        var idProducto = producto.id_producto;
                        
                        fetch(apiEndpoint + '/api/pedidos/remove_product_from_order', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                idOrder: idPedido,
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

                    tableProducto.appendChild(row);
                });
            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

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

// Logica boton Guardar Carrito
function guardarCarritoBoton() {
    var idPedido = localStorage.getItem('idPedido');
    fetch(apiEndpoint + '/api/pedidos/save_order', {
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