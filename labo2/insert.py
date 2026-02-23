from __future__ import annotations

import psycopg
import random

import time # para medir tiempos de inserción

from faker import Faker

from config import load_config

# Creo el generador Faker con locale español
# Pongo una semilla fija (123) para que siempre genere los mismos datos (reproducibilidad)
faker = Faker("es_ES")
Faker.seed(123)
faker.seed_instance(123)

# ----------------------------- 
num_profesores = 5 
num_cursos = 10 
num_alumnos = 15 
alumnos_por_curso = 3 # cuántos alumnos por curso

start = time.time() # para medir el tiempo total de inserción

def insert_profesor(nombre: str, email: str) -> int:
    """Inserta un profesor en la tabla `profesores` y devuelve su `profesor_id`.

    Parámetros:
    - nombre: nombre completo del profesor (cadena)
    - email: correo electrónico (cadena), la tabla tiene restricción UNIQUE

    Comportamiento:
    - Usa `RETURNING profesor_id` para obtener el id generado por SERIAL.
    - `load_config()` carga parámetros de conexión desde `database.ini`.
    - La conexión se abre con `psycopg.connect(**cfg)` y el contexto asegura
      commit/rollback automático al salir del bloque.
    """
    # Escribo la consulta SQL: uso %s como placeholders (seguro contra inyección SQL)
    sql = "INSERT INTO profesores(nombre, email) VALUES (%s, %s) RETURNING profesor_id;"

    # Leo los parámetros de conexión desde database.ini (host, puerto, BD, usuario, contraseña)
    cfg = load_config()

    # Me conecto a la BD y abro un cursor; el `with` cierra/guarda cambios automáticamente
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            # Ejecuto la consulta pasando los valores (nombre, email) como tupla
            cur.execute(sql, (nombre, email))
            # fetchone() me trae la fila; el id está en la posición 0 ([0])
            profesor_id = cur.fetchone()[0]

    return int(profesor_id)


def insert_curso(nombre: str, profesor_id: int) -> int:
    """Inserta un curso en `cursos` y devuelve `curso_id`.

    Parámetros:
    - nombre: nombre del curso (cadena)
    - profesor_id: clave foránea que referencia a `profesores.profesor_id` (int)

    Nota: la integridad referencial se delega a la BD; si `profesor_id` no existe,
    la base de datos lanzará un error de clave foránea.
    """
    # Inserto un curso con su profesor (profesor_id es clave foránea)
    sql = "INSERT INTO cursos(nombre, profesor_id) VALUES (%s, %s) RETURNING curso_id;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, profesor_id))
            # La BD me devuelve el id del curso recién creado
            curso_id = cur.fetchone()[0]
    return int(curso_id)


def insert_alumno(nombre: str, email: str) -> int:
    """Inserta un alumno en `alumnos` y devuelve `alumno_id`.

    Igual que `insert_profesor` pero para la tabla `alumnos`.
    """
    # Mismo patrón que insert_profesor, pero para alumnos
    sql = "INSERT INTO alumnos(nombre, email) VALUES (%s, %s) RETURNING alumno_id;"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, email))
            alumno_id = cur.fetchone()[0]
    return int(alumno_id)


def matricular(alumno_id: int, curso_id: int) -> None:
    """Crea una fila en `matriculas` que relaciona un `alumno` con un `curso`.

    Parámetros:
    - alumno_id: id del alumno (int)
    - curso_id: id del curso (int)

    Observaciones:
    - La PK es compuesta (alumno_id, curso_id) en `create_tables.py`.
    - Si la matrícula ya existe, la BD fallará por llave primaria duplicada.
    """
    # Creo la relación N:M entre alumno y curso en la tabla matriculas
    sql = "INSERT INTO matriculas(alumno_id, curso_id) VALUES (%s, %s);"
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (alumno_id, curso_id))


if __name__ == "__main__":
    # 1) Profesores - genero datos falsos con Faker (name() y safe_email())
    profesores_ids = []
    for _ in range(num_profesores):
        pid = insert_profesor(faker.name(), faker.safe_email())  # name() → nombre completo, safe_email() → email válido
        profesores_ids.append(pid)  # la BD lo genera automáticamente con SERIAL (numeros incrementales)

    # 2) Cursos - asigno cada curso a un profesor al azar
    cursos_ids = []
    for _ in range(num_cursos):
        profesor_id = random.choice(profesores_ids)  # selecciono profesor aleatorio
        cid = insert_curso(faker.word().capitalize(), profesor_id)  # word().capitalize() → palabra con mayúscula
        cursos_ids.append(cid)

    # 3) Alumnos - genero con datos falsos similares a profesores
    alumnos_ids = []
    for _ in range(num_alumnos):
        aid = insert_alumno(faker.name(), faker.safe_email())
        alumnos_ids.append(aid)

    # 4) Matrículas (N:M) - relaciono alumnos con cursos
    for curso_id in cursos_ids:
        alumnos_elegidos = random.sample(alumnos_ids, alumnos_por_curso)  # selecciono sin repetir
        for alumno_id in alumnos_elegidos:
            matricular(alumno_id, curso_id)  # creo la relación alumno-curso

    print("Datos insertados correctamente.")

    end = time.time() # tiempo final para medir el tiempo total de inserción
    print("Tiempo total:", end - start, "segundos")
