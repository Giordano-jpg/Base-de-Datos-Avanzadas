"""
Model (capa de acceso a datos).

- Centraliza la conexión a PostgreSQL usando config.load_config().
- Expone funciones de solo lectura (SELECT); devuelve objetos de dominio.
- No contiene HTML ni lógica de rutas; solo datos.

Si se cambia el motor o el esquema, solo se modifica este módulo.
"""
from __future__ import annotations

import psycopg

from config import load_config

from models.entities import Alumno, Curso, Matricula, Profesor


def get_connection():
    """
    Devuelve una conexión a PostgreSQL.

    Usa database.ini vía load_config(). La conexión debe usarse con
    context manager (with ... as conn) para cerrar correctamente.
    """
    cfg = load_config()
    return psycopg.connect(**cfg)

##############
# Profesores #
##############

# Detalle de un solo profesor (GET)
def get_profesor(profesor_id: int):
    """Devuelve un profesor por su id."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT profesor_id, nombre, email FROM profesores "
                "WHERE profesor_id=%s;",
                (profesor_id,)  # se pasa como parámetro para evitar SQL injection
            )
            # 'cur.fetchone()' devuelve una tupla con los datos del profesor o None si no existe
            r = cur.fetchone() # una tupla (profesor_id, nombre, email) o None
            if not r: # si no existe Profesor devuelve None
                return None
            return Profesor(id=r[0], nombre=r[1], email=r[2])

# Listado de profesores (GET)
def get_profesores():
    """Lista todos los profesores."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT profesor_id, nombre, email FROM profesores "
                "ORDER BY profesor_id;"
            )
            return [Profesor(id=r[0], nombre=r[1], email=r[2]) for r in cur.fetchall()]

# Detalle de un profesor y cursos que imparte (GET)
def get_cursos_profesor(profesor_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT curso_id, nombre, profesor_id FROM cursos "
                "WHERE profesor_id=%s;",
                (profesor_id,) # Se pasa el profesor_id como parámetro para evitar SQL injection
            )
            return [Curso(id=r[0], nombre=r[1], profesor_id=r[2]) for r in cur.fetchall()]

###########
# Alumnos #
###########

# Alta de un solo alumno (POST)
def create_alumno(nombre: str, email: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO alumnos (nombre, email) VALUES (%s, %s);",
                (nombre, email)
            )

# Detalle de un solo alumno (GET)
def get_alumno(alumno_id: int):
    """Devuelve un alumno por su id."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT alumno_id, nombre, email FROM alumnos "
                "WHERE alumno_id=%s;",
                (alumno_id,)
            )
            r = cur.fetchone() # una tupla (alumno_id, nombre, email) o None
            if not r: # si no existe Alumno devuelve None
                return None
            return Alumno(id=r[0], nombre=r[1], email=r[2])

# Listado de alumnos (GET)
def get_alumnos():
    """Lista todos los alumnos."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT alumno_id, nombre, email FROM alumnos "
                "ORDER BY alumno_id;"
            )
            return [Alumno(id=r[0], nombre=r[1], email=r[2]) for r in cur.fetchall()]

# Detalle de un alumno y cursos en los que esta matriculado (GET)
def get_cursos_alumno(alumno_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT c.curso_id, c.nombre, c.profesor_id FROM cursos c "
                "JOIN matriculas m ON c.curso_id = m.curso_id "
                "WHERE m.alumno_id = %s;",
                (alumno_id,)
            )
            return [Curso(id=r[0], nombre=r[1], profesor_id=r[2]) for r in cur.fetchall()]

##########
# Cursos #
##########

# Detalle de un solo curso (GET)
def get_curso(curso_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT curso_id, nombre, profesor_id FROM cursos "
                "WHERE curso_id=%s;",
                (curso_id,)
            )
            r = cur.fetchone() # una tupla (curso_id, nombre, profesor_id) o None
            if not r: # si no existe Curso devuelve None
                return None
            return Curso(id=r[0], nombre=r[1], profesor_id=r[2])

# Listado de cursos (GET)
def get_cursos():
    """Lista todos los cursos."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT curso_id, nombre, profesor_id FROM cursos "
                "ORDER BY curso_id;"
            )
            return [Curso(id=r[0], nombre=r[1], profesor_id=r[2]) for r in cur.fetchall()]

# Detalle de un curso y alumnos matriculados (GET)
def get_alumnos_curso(curso_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT a.alumno_id, a.nombre, a.email FROM alumnos a "
                "JOIN matriculas m ON a.alumno_id = m.alumno_id "
                "WHERE m.curso_id=%s;",
                (curso_id,)
            )
            return [Alumno(id=r[0], nombre=r[1], email=r[2]) for r in cur.fetchall()]

##############
# Matrículas #
##############

# Listado de matriculas (GET)
def get_matriculas():
    """Devuelve todas las matrículas de la tabla."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT alumno_id, curso_id, created_at FROM matriculas ORDER BY alumno_id, curso_id;"
            )
            return [Matricula(alumno_id=r[0], curso_id=r[1], created_at=r[2]) for r in cur.fetchall()]

# Matricular un alumno en curso (POST)
def create_matricula(alumno_id: int, curso_id: int):
    with get_connection() as conn:
        # Intento de matricular un alumna en un curso
        try: 
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO matriculas (alumno_id, curso_id) VALUES (%s, %s);",
                    (alumno_id, curso_id)
                )
                print(f"Alumno {alumno_id} matriculado en curso {curso_id}")
        # Si no existe se hace un rollback automático y se lanza una excepción
        except psycopg.errors.ForeignKeyViolation as exc:
            print(f"Foreign key violation -> ROLLBACK: alumno={alumno_id}, curso={curso_id}")
            raise # Se lanza la excepción (psycopg hace rollback automáticamente al detectar la excepción)

# Consulta 1: numero de cursos y alumnos distintos por profesor (GET)
def cursos_alumnos_profesor(profesor_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                -- Cursos y alumnos distintos
                SELECT COUNT(DISTINCT c.curso_id), COUNT(DISTINCT m.alumno_id)
                -- Tabla principal -> cursos
                FROM cursos c
                -- Une cada curso con las matrículas (alumnos) que tengan el mismo curso_id (si no hay matrícula, el curso igual se cuenta "NULL" en m.curso_id)
                LEFT JOIN matriculas m ON c.curso_id = m.curso_id
                -- Filtro por el profesor id = x
                WHERE c.profesor_id = %s;
                """,
                (profesor_id,)
            )
            r = cur.fetchone()
            return {"num_cursos": r[0], "num_alumnos": r[1]} # r[] es una tupla (num_cursos, num_alumnos)

# Consulta 2: número de cursos y profesores distintos por alumno (GET)
def cursos_profesores_alumno(alumno_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                -- Cursos y profesores distintos
                SELECT COUNT(DISTINCT c.curso_id), COUNT(DISTINCT c.profesor_id)
                -- Tabla principal -> matriculas
                FROM matriculas m
                -- Une cada matrícula con el curso que tenga el mismo curso_id (si no hay curso, la matrícula igual se cuenta "NULL" en c.curso_id)
                LEFT JOIN cursos c ON m.curso_id = c.curso_id
                -- Filtro por el alumno id = x
                WHERE m.alumno_id = %s;
                """,
                (alumno_id,)
            )
            r = cur.fetchone()
            return {"num_cursos": r[0], "num_profesores": r[1]} # r[] es una tupla (num_cursos, num_profesores)

