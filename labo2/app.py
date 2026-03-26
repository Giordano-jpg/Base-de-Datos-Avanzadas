"""
Punto de entrada de la aplicación (Application Factory).

- create_app() construye la instancia de Flask y registra blueprints y errores.
- Sin lógica de negocio: solo configuración y ensamblado.

Ejecución:
    export FLASK_APP=app.py
    flask run
"""
from __future__ import annotations

from flask import Flask, redirect, render_template, request, session, url_for

from routes import auth_bp, main_bp, profesores_bp, alumnos_bp, cursos_bp, matriculas_bp


def create_app() -> Flask:
    """Crea y configura la aplicación Flask (patrón factory)."""
    app = Flask(__name__)

    # Configuración mínima (evitar hardcodear en código)
    app.config["ENV"] = "development"
    app.config["SECRET_KEY"] = "1234"

    # Blueprints por recurso
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profesores_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(matriculas_bp)

    @app.before_request
    def require_login():
        if request.endpoint in (None, "auth.login", "static"):
            return None
        if request.endpoint and request.endpoint.startswith("auth."):
            return None
        if "username" not in session:
            return redirect(url_for("auth.login"))
        return None

    # Páginas de error (misma base que el resto)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app


# Instancia única para flask run y servidores WSGI
app = create_app()