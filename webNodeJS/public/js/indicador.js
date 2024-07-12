fetch('https://mindicador.cl/api').then(function(response) {
    return response.json();
}).then(function(dailyIndicators) {
    document.getElementById("UF").innerHTML = 'UF Hoy: $' + dailyIndicators.uf.valor;
}).catch(function(error) {
    console.log('Requestfailed', error);
});