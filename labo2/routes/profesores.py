"""Rutas del recurso profesores."""
from __future__ import annotations

from flask import Blueprint, render_template, abort

from models.db import get_profesores, get_cursos_profesor, get_profesor

profesores_bp = Blueprint("profesores", __name__, url_prefix="/profesores")

# Listado de profesores (GET)
@profesores_bp.route("")
def list_():
    """Lista de profesores. Datos desde el Model, presentación en la View."""
    profesores = get_profesores()
    # Lista de profesores en la plantilla profesores.html
    return render_template("profesores.html", profesores=profesores)

# Detalle de un profesor y cursos que imparte (GET)
@profesores_bp.route("/<int:id>")
def detail(id):
    """Detalle de un profesor y cursos que imparte."""
    profesor = get_profesor(id)
    if not profesor: # Si el profesor no existe, se muestra un error 404
        abort(404)
    cursos = get_cursos_profesor(id)
    # Detalle del profesor y los cursos que imparte en la plantilla cursos_profesor.html
    return render_template("cursos_profesor.html", profesor=profesor, cursos=cursos)