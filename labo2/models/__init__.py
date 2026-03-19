# Capa Model del MVC: acceso a datos (PostgreSQL) y entidades de dominio.

from models.db import (
    get_connection,
    get_profesores,
    get_profesor,
    get_alumnos,
    get_alumno,
    get_cursos,
    get_curso,
    get_cursos_alumno,
    get_alumnos_curso,
    get_cursos_profesor,
    get_matriculas,
    create_alumno,
    create_matricula,
)
from models.entities import Profesor, Alumno, Curso, Matricula

__all__ = [
    "Profesor",
    "Alumno",
    "Curso",
    "Matricula",
    "get_connection",
    "get_profesores",
    "get_profesor",
    "get_alumnos",
    "get_alumno",
    "get_cursos",
    "get_curso",
    "get_matriculas",
    "get_cursos_alumno",
    "get_alumnos_curso",
    "get_cursos_profesor",
    "create_alumno",
    "create_matricula",
]