"""Rutas del recurso cursos."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template

from models.db import get_cursos, get_curso, get_alumnos_curso

cursos_bp = Blueprint("cursos", __name__, url_prefix="/cursos")

# Listado de cursos (GET)
@cursos_bp.route("")
def list_():
    """Lista de cursos. Datos desde el Model, presentación en la View."""
    cursos = get_cursos()
    # Lista de cursos en la plantilla cursos.html
    return render_template("cursos.html", cursos=cursos)

# Detalle de un curso y alumnos matriculados (GET)
@cursos_bp.route("/<int:id>")
def detail(id):
    curso = get_curso(id) # función que devuelve un Curso o None
    if not curso: # Si el curso no existe, se muestra un error 404
        abort(404)
    alumnos = get_alumnos_curso(id)
    # Detalle del curso y los alumnos matriculados en la plantilla alumnos_curso.html
    return render_template("alumnos_curso.html", curso=curso, alumnos=alumnos)