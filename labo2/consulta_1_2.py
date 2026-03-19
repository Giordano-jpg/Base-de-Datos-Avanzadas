from models.db import cursos_alumnos_profesor, cursos_profesores_alumno

print("Consulta 1: (id del profesor = 2)", cursos_alumnos_profesor(2))
print("Consulta 2: (id del alumno = 2)", cursos_profesores_alumno(2))