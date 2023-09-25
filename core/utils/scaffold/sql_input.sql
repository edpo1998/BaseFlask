CREATE TABLE IF NOT EXISTS mprueba.roles
(
    cod_rol smallserial PRIMARY KEY,
    create_date timestamp(0) without time zone NOT NULL,
    update_date timestamp(0) without time zone,
    delete_date timestamp(0) without time zone,
    user_at smallint NOT NULL,
    activo boolean NOT NULL,
    nombre varchar(50) NOT NULL,
    usuario_cod smallint FOREIGN KEY REFERENCES mconfiguration.usuarios.cod_usuario

);