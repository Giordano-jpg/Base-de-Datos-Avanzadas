# Laboratorio 2 — Python + PostgreSQL (actualizado)

## 0) Preparación
```bash
python3 -m venv .venv # Windows: python -m venv .venv (solo la primera vez)
source .venv/bin/activate # Windows: .\.venv\Scripts\Activate.ps1
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
pip install -U pip
pip install -r requirements.txt
```

Edita `labo2/database.ini` con tus credenciales.

## 1) Parte A — Scripts (CRUD + transacciones + binarios)
Orden recomendado:
```bash
cd labo2
python connect.py
python create_tables.py
python insert.py
python update.py
python delete.py
python transaction.py
python write_blob.py
python read_blob.py
```

### 1.1) Función SQL (PSQL)
En `psql`, crea la función:

```sql
CREATE OR REPLACE FUNCTION get_parts_by_vendor(id INTEGER)
RETURNS TABLE(part_id INTEGER, part_name VARCHAR) AS
$$
BEGIN
  RETURN QUERY
  SELECT p.part_id, p.part_name
  FROM parts p
  INNER JOIN vendor_parts vp ON vp.part_id = p.part_id
  WHERE vp.vendor_id = id;
END;
$$ LANGUAGE plpgsql;
```

Luego:
```bash
python call_function.py
```

### 1.2) Procedimiento almacenado (PSQL)
En `psql`, crea el procedimiento:

```sql
CREATE OR REPLACE PROCEDURE add_new_part(new_part_name varchar, new_vendor_name varchar)
LANGUAGE plpgsql
AS $$
DECLARE
  v_part_id INT;
  v_vendor_id INT;
BEGIN
  INSERT INTO parts(part_name) VALUES(new_part_name) RETURNING part_id INTO v_part_id;
  INSERT INTO vendors(vendor_name) VALUES(new_vendor_name) RETURNING vendor_id INTO v_vendor_id;
  INSERT INTO vendor_parts(vendor_id, part_id) VALUES(v_vendor_id, v_part_id);
END;
$$;
```

Luego:
```bash
python call_stored_procedure.py
```

## 2) Parte B — FAKE (datos sintéticos)
```bash
cd ../fake
python fake.py
```

El script muestra:
- **Locales** (idioma/cultura del dato generado)
- **Semilla** para reproducibilidad
- **Generación por lotes** (no imprimir dentro de bucles grandes)

## Diagrama Entidad–Relación 

Aquí se muestra el modelo ER utilizado en la práctica:

<img src="https://github.com/user-attachments/assets/77f6a4f2-e7c0-44ae-88f6-579aacd6202a" width="65%">
