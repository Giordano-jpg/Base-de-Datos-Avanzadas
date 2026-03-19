from __future__ import annotations

import psycopg
from psycopg import errors

from config import load_config

from models.db import create_matricula

# Caso válido
try:
    create_matricula(1, 1)  # alumno y curso existentes
except Exception as exc:
    print("Error:", exc)

# Caso intencionado (fallo/rollback)
try:
    create_matricula(1, 999999)  # curso que no existe
except Exception:
    print("Transacción fallida como se esperaba, no hay datos parciales.")


'''def add_matricula_atomic(alumno_id: int, curso_ids: list[int]):
    """Single atomic operation: insert ONE matricula and assign it to ONE or more cursos.

    If curso_id does not exist, the whole operation fails and nothing is inserted.
    """
    sql = "INSERT INTO matriculas (alumno_id, curso_id) VALUES (%s, %s);"

    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        try:
            with conn.cursor() as cur:
                for curso_id in curso_ids:
                    cur.execute(sql, (alumno_id, curso_id))
                print("Transacción completada")
        except errors.ForeignKeyViolation as exc:
            print("Foreign key violation -> ROLLBACK:", exc)
            raise


if __name__ == "__main__":
    # Example 1: atomic operation (should succeed if alumno_id=1 and curso_id=1 exist)
    try:
        add_matricula_atomic(1, [1])
        print(f"Alumno {alumno_id} matriculado en curso {curso_id}")
    except Exception as exc:
        print("Error:", exc)

    # Example 2: transactional flow (force a failure with a non-existing curso id)
    try:
        add_matricula_atomic(1, [1, 999999])
    except Exception:
        print(f"Transactional flow failed as expected. Intentó matricular {alumno_id} en cursos {curso_ids}, but no partial data was inserted.")
        '''