"""Rutas del recurso de matriculas."""
from __future__ import annotations

from flask import Blueprint, Response, abort, render_template, request, redirect, url_for

from models.db import get_matriculas, create_matricula

matriculas_bp = Blueprint("matriculas", __name__, url_prefix="/matriculas")

# Listado de matriculas (GET)
@matriculas_bp.route("")
def list_():
    """Lista de matriculas. Datos desde el Model, presentación en la View."""
    matriculas = get_matriculas()
    return render_template("matriculas.html", matriculas=matriculas)

# Matricular un alumno en curso (POST)
@matriculas_bp.route("/nuevo", methods=["GET", "POST"]) # GET para mostrar el formulario, POST para procesar el formulario
def create():
    # Si el método es POST, se crea la matrícula con los datos del formulario
    if request.method == "POST":
        alumno_id = request.form.get("alumno_id") # request.form.get() obtiene el valor del input con name="alumno_id" en el formulario
        curso_id = request.form.get("curso_id") # request.form.get() obtiene el valor del input con name="curso_id" en el formulario
        # Convierto a 'int' porque 'create_matricula(alumno_id: int, curso_id: int)' espera enteros:
        create_matricula(int(alumno_id), int(curso_id))
        # Redirige a la lista de matriculas
        return redirect(url_for("matriculas.list_"))
    # si es GET, mostrar el formulario
    return render_template("create_matricula.html")