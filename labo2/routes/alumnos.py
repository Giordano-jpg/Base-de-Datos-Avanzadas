"""Rutas del recurso alumnos."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_alumnos, get_alumno, get_cursos_alumno, create_alumno

alumnos_bp = Blueprint("alumnos", __name__, url_prefix="/alumnos")

# Listado de alumnos (GET)
@alumnos_bp.route("")
def list_():
    """Lista de alumnos. Datos desde el Model, presentación en la View."""
    alumnos = get_alumnos()
    # Lista de alumnos en la plantilla alumnos.html
    return render_template("alumnos.html", alumnos=alumnos)

# Detalle de un alumno y cursos en los que esta matriculado (GET)
@alumnos_bp.route("/<int:id>")
def detail(id):
    """Detalle de un alumno y cursos en los que está matriculado."""
    alumno = get_alumno(id) # función que devuelve un Alumno o None
    if not alumno:
        abort(404) # Si el alumno no existe, se muestra un error 404
    cursos = get_cursos_alumno(id)
    # Detalle del alumno y los cursos en los que está matriculado en la plantilla cursos_alumno.html
    return render_template("cursos_alumno.html", alumno=alumno, cursos=cursos)

# Alta de un alumno (POST)
@alumnos_bp.route("/nuevo", methods=["GET", "POST"]) # GET para mostrar el formulario, POST para procesar el formulario
def create():
    # Si el método es POST, se crea el alumno con los datos del formulario
    if request.method == "POST":
        nombre = request.form.get("nombre") # request.form.get() obtiene el valor del input con name="nombre" en el formulario
        email = request.form.get("email") # request.form.get() obtiene el valor del input con name="email" en el formulario
        create_alumno(nombre, email)
        # Redirige a la lista de alumnos después de crear el alumno
        return redirect(url_for("alumnos.list_"))
    # si es GET, mostrar el formulario
    return render_template("create_alumno.html")