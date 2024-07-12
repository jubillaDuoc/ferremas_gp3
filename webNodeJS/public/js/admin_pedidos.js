var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {

    fetch(apiEndpoint + '/api/pedidos/get_orders', {
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

                data.orders.forEach(order => {
                    var row = document.createElement('tr');

                    var idCell = document.createElement('td');
                    var link = document.createElement('a');
                    link.textContent = order.id_pedido;
                    link.href = '/edit_pedido?idPedido=' + order.id_pedido;
                    idCell.appendChild(link);
                    row.appendChild(idCell);

                    var estadoCell = document.createElement('td');
                    estadoCell.textContent = order.nombre_estado_pedido;
                    row.appendChild(estadoCell);

                    var userCell = document.createElement('td');
                    userCell.textContent = order.email_user;
                    row.appendChild(userCell);
                    
                    var userRolCell = document.createElement('td');
                    userRolCell.textContent = order.nombre_user_rol;
                    row.appendChild(userRolCell);

                    var userStateCell = document.createElement('td');
                    userStateCell.textContent = order.nombre_user_state;
                    row.appendChild(userStateCell);

                    var orderTotalCell = document.createElement('td');
                    orderTotalCell.textContent = order.total_pedido;
                    row.appendChild(orderTotalCell);


                    // Editar Pedido
                    var accionesCell = document.createElement('td');
                    var agregarButton = document.createElement('button');
                    agregarButton.textContent = 'Modificar';
                    agregarButton.classList.add('btn', 'btn-secondary');
                    agregarButton.addEventListener('click', () => {
                        window.location.href = '/edit_pedido?idPedido=' + order.id_pedido;
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