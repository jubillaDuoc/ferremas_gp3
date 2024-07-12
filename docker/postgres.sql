/*
-- USERS!!!

DROP VIEW USERS_VIEW;
DROP TABLE USERS_ROLE CASCADE;
DROP TABLE USERS_STATE CASCADE;
DROP TABLE USERS CASCADE;
DROP TABLE USERS_TOKEN CASCADE;
DROP TABLE WEB_SESSIONS CASCADE;

-- PRODUCTOS!!!
DROP VIEW PRODUCTO_VIEW;
DROP TABLE TIPO_PRODUCTO CASCADE;
DROP TABLE SUBTIPO_PRODUCTO CASCADE;
DROP TABLE MARCA_PRODUCTO CASCADE;
DROP TABLE PRODUCTO CASCADE;
DROP TABLE PRECIO_PRODUCTO CASCADE;

-- PEDIDOS!!!
DROP VIEW PEDIDO_VIEW;
DROP VIEW PEDIDO_PRODUCTO_VIEW;
DROP TABLE ESTADO_PEDIDO CASCADE;
DROP TABLE PEDIDO CASCADE;
DROP TABLE PEDIDO_PRODUCTO CASCADE;
*/

CREATE TABLE USERS_ROLE (
    id_user_rol       SERIAL PRIMARY KEY,
    nombre_user_rol     VARCHAR(200) NOT NULL
);

INSERT INTO USERS_ROLE ("nombre_user_rol") VALUES
('admin'),
('vendedor'),
('bodega'),
('contabilidad'),
('cliente');

CREATE TABLE USERS_STATE (
    id_user_state       SERIAL PRIMARY KEY,
    nombre_user_state   VARCHAR(200) NOT NULL
);

INSERT INTO USERS_STATE ("id_user_state", "nombre_user_state") VALUES
(1, 'Active'),
(2, 'Inactive'),
(3, 'Blocked'),
(4, 'Deleted');

CREATE TABLE USERS (
    id_user         SERIAL PRIMARY KEY,
    nombre_user     VARCHAR(200) NOT NULL,
    email_user      VARCHAR(200) NOT NULL,
    passwd_user     VARCHAR(200) NOT NULL,
    id_user_rol    INTEGER NOT NULL REFERENCES USERS_ROLE,
    id_user_state   INTEGER NOT NULL REFERENCES USERS_STATE
);
INSERT INTO "users" ("id_user", "nombre_user", "email_user", "passwd_user", "id_user_rol", "id_user_state") VALUES
(1,	'José Ubilla',	'jose.ubilla073@gmail.com',	'eBnGu2KTA2dWtcSCpybt1gGo/iRWAjmVJB7zBgzeeI8=',	1,	1);

CREATE TABLE USERS_TOKEN (
    token_session           TEXT PRIMARY KEY,
    created_at_session      TIMESTAMP NOT NULL,
    valid_from_session      TIMESTAMP NOT NULL,
    valid_to_session        TIMESTAMP NOT NULL,
    id_user                 INTEGER NOT NULL REFERENCES USERS
);

CREATE TABLE WEB_SESSIONS (
    token_web           TEXT PRIMARY KEY,
    created_at_web      TIMESTAMP NOT NULL,
    valid_from_web      TIMESTAMP NOT NULL,
    valid_to_web        TIMESTAMP NOT NULL,
    id_user             INTEGER REFERENCES USERS
);

CREATE VIEW USERS_VIEW AS
SELECT
    u.id_user,
    u.nombre_user,
    u.passwd_user,
    u.email_user,
    u.id_user_rol,
    ur.nombre_user_rol,
    u.id_user_state,
    us.nombre_user_state
FROM
    USERS u
    JOIN USERS_ROLE ur ON u.id_user_rol = ur.id_user_rol
    JOIN USERS_STATE us ON u.id_user_state = us.id_user_state;

CREATE TABLE TIPO_PRODUCTO (
    id_tipo_producto         SERIAL PRIMARY KEY,
    nombre_tipo_producto       VARCHAR(200) NOT NULL
);

CREATE TABLE SUBTIPO_PRODUCTO (
    id_subtipo_producto         SERIAL PRIMARY KEY,
    nombre_subtipo_producto     VARCHAR(200) NOT NULL,
    id_tipo_producto            INTEGER NOT NULL REFERENCES TIPO_PRODUCTO
);

CREATE TABLE MARCA_PRODUCTO (
    id_marca_producto       SERIAL PRIMARY KEY,
    nombre_marca_producto   VARCHAR(200) NOT NULL
);

CREATE TABLE PRODUCTO (
    id_producto             SERIAL PRIMARY KEY,
    nombre_producto         VARCHAR(200) NOT NULL,
    stock_producto          INTEGER NOT NULL,
    id_subtipo_producto     INTEGER NOT NULL REFERENCES SUBTIPO_PRODUCTO,
    id_marca_producto       INTEGER NOT NULL REFERENCES MARCA_PRODUCTO
);

CREATE TABLE PRECIO_PRODUCTO (
    id_precio_producto      SERIAL PRIMARY KEY,
    id_producto             INTEGER NOT NULL REFERENCES PRODUCTO,
    precio_producto         NUMERIC NOT NULL,
    fecha_precio_producto   TIMESTAMP NOT NULL
); 

CREATE VIEW PRODUCTO_VIEW AS
SELECT
    p.id_producto,
    p.nombre_producto,
    p.stock_producto,
    pp.precio_producto,
    pp.fecha_precio_producto,
    p.id_subtipo_producto,
    sp.nombre_subtipo_producto,
    sp.id_tipo_producto,
    tp.nombre_tipo_producto,
    p.id_marca_producto,
    mp.nombre_marca_producto
FROM
    PRODUCTO p
    JOIN SUBTIPO_PRODUCTO sp ON p.id_subtipo_producto = sp.id_subtipo_producto
    JOIN TIPO_PRODUCTO tp ON sp.id_tipo_producto = tp.id_tipo_producto
    JOIN MARCA_PRODUCTO mp ON p.id_marca_producto = mp.id_marca_producto
    JOIN (
        SELECT
        id_producto,
        MAX(id_precio_producto) AS max_id_precio_producto
        FROM PRECIO_PRODUCTO
        GROUP BY id_producto
    ) AS latest_price ON p.id_producto = latest_price.id_producto
    JOIN PRECIO_PRODUCTO pp ON latest_price.max_id_precio_producto = pp.id_precio_producto;

-- PEDIDOS!!!

CREATE TABLE ESTADO_PEDIDO (
    id_estado_pedido         SERIAL PRIMARY KEY,
    nombre_estado_pedido     VARCHAR(200) NOT NULL
);

INSERT INTO ESTADO_PEDIDO ("nombre_estado_pedido") VALUES
('Tomado por usuario'),
('En facturacion'),
('En proceso'),
('Enviado'),
('Entregado'),
('Cancelado');

CREATE TABLE PEDIDO (
    id_pedido           SERIAL PRIMARY KEY,
    id_user             INTEGER NOT NULL REFERENCES USERS,
    fecha_pedido        TIMESTAMP NOT NULL,
    total_pedido        NUMERIC NOT NULL,
    id_estado_pedido    INTEGER NOT NULL REFERENCES ESTADO_PEDIDO
);

CREATE TABLE PEDIDO_PRODUCTO (
    id_pedido_producto   SERIAL PRIMARY KEY,
    id_pedido            INTEGER NOT NULL REFERENCES PEDIDO,
    id_producto          INTEGER NOT NULL REFERENCES PRODUCTO,
    cantidad_producto    INTEGER NOT NULL,
    precio_producto      NUMERIC NOT NULL
);

CREATE VIEW PEDIDO_PRODUCTO_VIEW AS
SELECT
    pp.id_pedido_producto,
    pp.id_pedido,
    pp.id_producto,
    pr.nombre_producto,
    pp.cantidad_producto,
    pp.precio_producto,
    pd.fecha_pedido,
    pd.total_pedido,
    pd.id_estado_pedido,
    ep.nombre_estado_pedido
FROM
    PEDIDO_PRODUCTO pp
    JOIN PRODUCTO pr ON pp.id_producto = pr.id_producto
    JOIN PEDIDO pd ON pp.id_pedido = pd.id_pedido
    JOIN ESTADO_PEDIDO ep ON pd.id_estado_pedido = ep.id_estado_pedido;

CREATE VIEW PEDIDO_VIEW AS
SELECT 
    p.id_pedido,
    p.fecha_pedido,
    p.total_pedido,
    p.id_estado_pedido,
    ep.nombre_estado_pedido,
    uv.id_user,
    uv.nombre_user,
    uv.email_user,
    uv.id_user_rol,
    uv.nombre_user_rol,
    uv.id_user_state,
    uv.nombre_user_state
FROM
    pedido p
    JOIN estado_pedido ep ON p.id_estado_pedido = ep.id_estado_pedido
    JOIN users_view uv ON p.id_user = uv.id_user;

--ALTER TABLE PEDIDO
--ADD COLUMN id_pedido_producto INTEGER REFERENCES PEDIDO_PRODUCTO;

COMMIT;
