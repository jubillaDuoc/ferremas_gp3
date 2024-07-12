var apiEndpoint = localStorage.getItem('apiEndpoint');

document.addEventListener('DOMContentLoaded', (event) => {
    fetch(apiEndpoint + '/api/productos/get_tipos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: localStorage.getItem('user_token') }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.check_token === true) {
        var container = document.getElementById('cardsTipos');
        localStorage.setItem('check_token', true);
        data.tipos.forEach(tipo => {
          var col = document.createElement('div');
          col.className = 'col';
  
          var a = document.createElement('a');
          a.href = '/productos?idtipo=' + tipo.id_tipo_producto;
          a.style.textDecoration = 'none';
          a.style.color = 'inherit';
  
          var card = document.createElement('div');
          card.className = 'card h-100';
  
          var cardBody = document.createElement('div');
          cardBody.className = 'card-body';
  
          var cardText = document.createElement('p');
          cardText.className = 'card-text';
          cardText.textContent = tipo.nombre_tipo_producto;
  
          cardBody.appendChild(cardText);
          card.appendChild(cardBody);
          a.appendChild(card);
          col.appendChild(a);
          container.appendChild(col);
        });
      } else {
        console.log('Token not valid');
        localStorage.setItem('check_token', false);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });