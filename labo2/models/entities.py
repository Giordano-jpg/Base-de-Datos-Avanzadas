"""
Objetos de dominio: tipos claros para la capa de presentación.

La vista y el controlador trabajan con Profesores, Alumnos, Cursos y Matrículas, no con tuplas.
"""
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Profesor:
    id: int
    nombre: str
    email: str

@dataclass(frozen=True)
class Alumno:
    id: int
    nombre: str
    email: str

@dataclass(frozen=True)
class Curso:
    id: int
    nombre: str
    profesor_id: int

@dataclass(frozen=True)
class Matricula:
    alumno_id: int
    curso_id: int
    created_at: str


'''@dataclass(frozen=True)
class Vendor:
    """Proveedor (vendor)."""
    id: int
    name: str


@dataclass(frozen=True)
class Part:
    """Pieza (part)."""
    id: int
    name: str
'''