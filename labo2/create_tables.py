from __future__ import annotations

import psycopg

from config import load_config



DDL = (
    """
    -- Tabla profesores: profesor_id (PK), nombre, email (único)

    CREATE TABLE IF NOT EXISTS profesores (
        profesor_id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    );
    """,
    """
    -- Tabla cursos: curso_id (PK), nombre, profesor_id (FK a profesores)

    CREATE TABLE IF NOT EXISTS cursos (
        curso_id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        profesor_id INTEGER NOT NULL,
        FOREIGN KEY (profesor_id)
            REFERENCES profesores(profesor_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    """,
    """
    -- Tabla alumnos: alumno_id (PK), nombre, email (único)

    CREATE TABLE IF NOT EXISTS alumnos (
        alumno_id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    );
    """,
    """
    -- Tabla matriculas: relación N:M entre alumnos y cursos (PK compuesta: alumno_id, curso_id)

    CREATE TABLE IF NOT EXISTS matriculas (
        alumno_id INTEGER NOT NULL,
        curso_id INTEGER NOT NULL,
        PRIMARY KEY (alumno_id, curso_id),
        FOREIGN KEY (alumno_id)
            REFERENCES alumnos(alumno_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (curso_id)
            REFERENCES cursos(curso_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    """
)


def create_tables() -> None:
    """Create demo tables for the lab (idempotent)."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
    print("Tables created (or already existed).")


if __name__ == "__main__":
    create_tables()
