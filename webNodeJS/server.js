const express = require('express');
const path = require('path');
const app = express();
const hostname = '0.0.0.0';
const port = 3000;

// Middleware para agregar datos al objeto de respuesta
app.use((req, res, next) => {
  // Puedes configurar datos que desees almacenar en localStorage
  // Por ejemplo, un token de sesión o información de usuario.
  res.locals.localStorageData = {
    apiEndpoint: 'http://172.26.203.78:5000'
  };
  next();
});

// Configurar el motor de plantillas EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Servir archivos estáticos desde la carpeta "public"
app.use(express.static(path.join(__dirname, 'public')));

// Importar las rutas
const routes = require('./routes');
app.use(routes);

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://${hostname}:${port}/`);
});
