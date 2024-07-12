var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {
    var urlParams = new URLSearchParams(window.location.search);
    var idProducto = urlParams.get('idProducto');
    var element;
    var USD = localStorage.getItem('usdvalue');

    fetch(apiEndpoint + '/api/productos/get_producto_by_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_producto: idProducto,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);

                var producto = data.producto;

                console.log('idProducto ' + data.producto.id_producto);

                element = document.getElementById('idProducto')
                element.textContent = producto.id_producto;

                element = document.getElementById('nombreProducto')
                element.textContent = producto.nombre_producto;

                element = document.getElementById('nombreMarcaProducto')
                element.textContent = producto.nombre_marca_producto;

                element = document.getElementById('nombreTipoProducto')
                element.textContent = producto.nombre_tipo_producto;

                element = document.getElementById('nombreSubtipoProducto')
                element.textContent = producto.nombre_subtipo_producto;

                element = document.getElementById('precioCLPProducto')
                element.textContent = producto.precio_producto;

                element = document.getElementById('precioUSDProducto')
                element.textContent = (producto.precio_producto / USD).toFixed(2);

                element = document.getElementById('stockProducto')
                element.textContent = producto.stock_producto;

                element = document.getElementById('accionProducto')
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
                element.appendChild(agregarButton);
                

            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});