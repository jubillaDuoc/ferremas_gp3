var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {
    var urlParams = new URLSearchParams(window.location.search);
    var idTipo = urlParams.get('idtipo');
    var USD = localStorage.getItem('usdvalue');

    fetch(apiEndpoint + '/api/productos/get_productos_by_tipo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_tipo: idTipo,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);
                var tableBody = document.getElementById('resultado-tabla');
                var titlePag = document.getElementById('titlePag');
                titlePag.textContent = 'Herramientas por tipo';

                data.productos.forEach(producto => {
                    var row = document.createElement('tr');

                    var nombreProductoCell = document.createElement('td');
                    var link = document.createElement('a');
                    link.textContent = producto.nombre_producto;
                    link.href = '/detalle_producto?idProducto=' + producto.id_producto;
                    nombreProductoCell.appendChild(link);
                    row.appendChild(nombreProductoCell);

                    var marcaCell = document.createElement('td');
                    marcaCell.textContent = producto.nombre_marca_producto;
                    row.appendChild(marcaCell);

                    var subTipoCell = document.createElement('td');
                    subTipoCell.textContent = producto.nombre_subtipo_producto;
                    row.appendChild(subTipoCell);

                    var stockCell = document.createElement('td');
                    stockCell.textContent = producto.stock_producto;
                    row.appendChild(stockCell);

                    var precioCell = document.createElement('td');
                    precioCell.textContent = producto.precio_producto;
                    row.appendChild(precioCell);

                    var precioCell = document.createElement('td');
                    precioCell.textContent = (producto.precio_producto / USD).toFixed(2);
                    row.appendChild(precioCell);

                    // Agregar al carrito
                    var accionesCell = document.createElement('td');
                    var agregarButton = document.createElement('button');
                    agregarButton.textContent = 'Agregar al carrito';
                    agregarButton.addEventListener('click', function() {
                        var productData = {
                            id_producto: producto.id_producto,
                            cantidad_producto: 1, // You can set the desired quantity here
                            precio_producto: producto.precio_producto
                        };
                        var idPedido = localStorage.getItem('idPedido');
                        if (idPedido !== "undefined" && idPedido !== null) {
                            fetch(apiEndpoint + '/api/pedidos/add_product_to_order', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    token: localStorage.getItem('user_token'),
                                    idOrder: idPedido,
                                    product: productData
                                }),
                            })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.check_token === true) {
                                        localStorage.setItem('check_token', true);
                                        console.log('Producto agregado al carrito');
                                    } else {
                                        localStorage.setItem('check_token', false);
                                        console.log('Token not valid');
                                    }
                                })
                                .catch((error) => {
                                    console.error('Error:', error);
                                });
                        } else {
                            fetch(apiEndpoint + '/api/pedidos/create_order', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    token: localStorage.getItem('user_token'),
                                    mailUser: localStorage.getItem('username'),
                                    product: productData
                                }),
                            })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.check_token === true) {
                                        localStorage.setItem('check_token', true);
                                        localStorage.setItem('idPedido', data.idPedido);
                                        console.log('Producto agregado al carrito');
                                    } else {
                                        localStorage.setItem('check_token', false);
                                        console.log('Token not valid');
                                    }
                                })
                                .catch((error) => {
                                    console.error('Error:', error);
                                });
                        }
                    });
                    accionesCell.appendChild(agregarButton);
                    row.appendChild(accionesCell);

                    tableBody.appendChild(row);
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