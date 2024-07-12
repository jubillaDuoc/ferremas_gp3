var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {
    var urlParams = new URLSearchParams(window.location.search);
    var idProducto = urlParams.get('idProducto');

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

                element = document.getElementById('nombreProductoInput')
                element.value = producto.nombre_producto;

                fetch(apiEndpoint + '/api/productos/get_marcas', {
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

                        var marcas = data.marcas;

                        var selectMarcas = document.getElementById('nombreMarcaProducto');
                        selectMarcas.innerHTML = '';

                        marcas.forEach(marca => {
                            var optionElement = document.createElement('option');
                            optionElement.value = marca.id_marca_producto;
                            optionElement.textContent = marca.nombre_marca_producto;
                            if (marca.id_marca_producto === producto.id_marca_producto) {
                                optionElement.selected = true;
                            }
                            selectMarcas.appendChild(optionElement);
                        });
                    } else {
                        localStorage.setItem('check_token', false);
                        console.log('Token not valid');
                    }
                }).catch((error) => {
                    console.error('Error:', error);
                });

                fetch(apiEndpoint + '/api/productos/get_tipos', {
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

                        var tipos = data.tipos;

                        var tipoSelect = document.getElementById('nombreTipoProducto');
                        tipoSelect.innerHTML = '';

                        tipos.forEach(tipo => {
                            var optionElement = document.createElement('option');
                            optionElement.value = tipo.id_tipo_producto;
                            optionElement.textContent = tipo.nombre_tipo_producto;
                            optionElement.disabled = true; // Disable the option
                            if (tipo.id_tipo_producto === producto.id_tipo_producto) {
                                optionElement.selected = true;
                            }
                            tipoSelect.appendChild(optionElement);
                        });
                    } else {
                        localStorage.setItem('check_token', false);
                        console.log('Token not valid');
                    }
                }).catch((error) => {
                    console.error('Error:', error);
                });

                fetch(apiEndpoint + '/api/productos/get_subtipos', {
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

                        var subtipos = data.subtipos;

                        var subtipoSelect = document.getElementById('nombreSubtipoProducto');
                        subtipoSelect.innerHTML = '';

                        subtipos.forEach(subtipo => {
                            var optionElement = document.createElement('option');
                            optionElement.value = subtipo.id_subtipo_producto;
                            optionElement.textContent = subtipo.nombre_subtipo_producto;
                            if (subtipo.id_subtipo_producto === producto.id_subtipo_producto) {
                                optionElement.selected = true;
                            }
                            subtipoSelect.appendChild(optionElement);
                        });
                    } else {
                        localStorage.setItem('check_token', false);
                        console.log('Token not valid');
                    }
                }).catch((error) => {
                    console.error('Error:', error);
                });

                element = document.getElementById('precioProductoInput')
                element.value = producto.precio_producto;

                element = document.getElementById('stockProductoInput')
                element.value = producto.stock_producto;
                
                element = document.getElementById('accionProducto')
                element.innerHTML = '<button type="button" class="btn btn-primary" onclick="send_data_product()">Guardar</button>';

            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

// Función para enviar los datos del producto a /api/productos/edit_producto
function send_data_product() {
    var idProducto = document.getElementById('idProducto').textContent;
    var nombreProducto = document.getElementById('nombreProductoInput').value;
    var nombreMarcaProducto = document.getElementById('nombreMarcaProducto').value;
    var nombreTipoProducto = document.getElementById('nombreTipoProducto').value;
    var nombreSubtipoProducto = document.getElementById('nombreSubtipoProducto').value;
    var precioProducto = document.getElementById('precioProductoInput').value;
    var stockProducto = document.getElementById('stockProductoInput').value;

    // Check Precio y Stock
    // Verificar si el precio es flotante o alert y return
    if (isNaN(precioProducto)){
        alert('Precio no es un número');
        return;
    }
    if (precioProducto < 0) {
        precioProducto = 0;
    }
    // Verificar si el stock es numero o alert y return
    if (isNaN(stockProducto)){
        alert('Stock no es un número');
        return;
    }
    if (stockProducto < 0) {
        stockProducto = 0;
    }

    fetch(apiEndpoint + '/api/productos/update_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_producto: idProducto,
            nombre_producto: nombreProducto,
            id_marca: nombreMarcaProducto,
            id_tipo: nombreTipoProducto,
            id_subtipo: nombreSubtipoProducto,
            precio_producto: precioProducto,
            stock_producto: stockProducto,
            token: localStorage.getItem('user_token')
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.check_token === true) {
                localStorage.setItem('check_token', true);
                console.log('Producto editado');
                window.location.href = '/admin_productos';
            } else {
                localStorage.setItem('check_token', false);
                console.log('Token not valid');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Mostrar mensaje de error
            alert('Error al editar el producto');
            return;
        });

}