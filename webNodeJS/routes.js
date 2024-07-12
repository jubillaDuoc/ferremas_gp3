const express = require('express');
const router = express.Router();

// Ruta principal que sirve el archivo index.ejs
router.get('/', (req, res) => {
    res.render('index');
  });

// ##Vistas de Productos
// Listar productos
router.get('/productos', (req, res) => {
  res.render('productos');
});

// Detalle de producto
router.get('/detalle_producto', (req, res) => {
  res.render('detalle_producto');
});

// ##Vistas de Pedidos
// Carrito de compras
router.get('/carrito', (req, res) => {
  res.render('carrito');
});

// Checkout

// Confirmación de pedido

// Historial de pedidos



// ##Vistas de Administrador
// Admin Pedidos
router.get('/admin_pedidos', (req, res) => {
  res.render('admin_pedidos');
});

// Edit Pedido edit_pedido
router.get('/edit_pedido', (req, res) => {
  res.render('edit_pedido');
});

// Admin Productos
router.get('/admin_productos', (req, res) => {
  res.render('admin_productos');
});

// Edit Productos edit_producto
router.get('/edit_producto', (req, res) => {
  res.render('edit_producto');
});

// Add Productos add_producto
router.get('/add_producto', (req, res) => {
  res.render('add_producto');
});

// Admin Usuarios
router.get('/admin_usuarios', (req, res) => {
  res.render('admin_usuarios');
});

// Edit Usuario
router.get('/edit_usuario', (req, res) => {
  res.render('edit_usuario');
});

// Add Usuario
router.get('/add_usuario', (req, res) => {
  res.render('add_usuario');
});

// ##Vistas de Usuarios
// Login
router.get('/login', (req, res) => {
  res.render('login');
});

// Registro
router.get('/signup', (req, res) => {
  res.render('signup');
});

// Perfil
router.get('/user_manager', (req, res) => {
  res.render('user_manager');
});

module.exports = router;
