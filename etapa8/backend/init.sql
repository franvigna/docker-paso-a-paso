-- Crea la tabla si no existe (se ejecuta solo la primera vez)
CREATE TABLE IF NOT EXISTS becarios (
    id            SERIAL PRIMARY KEY,
    dni           VARCHAR(10)  NOT NULL UNIQUE,
    nombre        VARCHAR(100) NOT NULL,
    apellido      VARCHAR(100) NOT NULL,
    fecha_ingreso DATE         NOT NULL,
    categoria     VARCHAR(20)  NOT NULL CHECK (categoria IN ('Inicial','Intermedio','Superior','Líder','Senior'))
);
