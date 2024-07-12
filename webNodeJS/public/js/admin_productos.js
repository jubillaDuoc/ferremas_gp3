var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {

    fetch(apiEndpoint + '/api/productos/get_productos_by_admin', {
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

                data.productos.forEach(producto => {
                    var row = document.createElement('tr');

                    var idCell = document.createElement('td');
                    idCell.textContent = producto.id_producto;
                    row.appendChild(idCell);

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

                    // Agregar al carrito
                    var accionesCell = document.createElement('td');
                    var agregarButton = document.createElement('button');
                    agregarButton.textContent = 'Modificar';
                    agregarButton.classList.add('btn', 'btn-secondary');
                    agregarButton.addEventListener('click', () => {
                        window.location.href = '/edit_producto?idProducto=' + producto.id_producto;
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