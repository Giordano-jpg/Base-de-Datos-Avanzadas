# Requisitos previos
1. Tener instalado Docker Desktop (para windows 11 con WSL)
2. Comprobar que está instalado: (bash)
```bash
docker --version
```
3. Instalar airflow (o situiarse en la carpeta si ya lo está):
```bash
mkdir airflow
cd airflow
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/x.x.x/docker-compose.yaml'
```
4. Crear archivo de variables de entorno (.env)
```bash
touch .env
nano .env
```
Dentro de `.env`, añadir lo siguiente:
```env
AIRFLOW_UID=50000     # UID para evitar problemas de permisos en Docker
FERNET_KEY=           # Clave de cifrado (vacía para pruebas)
```
> Opcional; para no tener que ejecutar `sudo` para cada instrucción o tener problemas de permiso al editar código dentro de Airflow, **ejecutar**: 
```bash
sudo chown -R $USER:$USER ~/Documentos/airflow
sudo usermod -aG docker $USER
```
> (Reiniciar para aplicar el cambio de la ultima instruccion)

5. Inicializar Airflow (solo la primera vez):
```bash
docker compose up airflow-init
```

# Estructura del proyecto
```
airflow/
├── docker-compose.yaml
├── dags/
│   ├── dag_de_usuarios.py
│   ├── postgres_pipeline_simple.py
│   └── scripts/
│       ├── config.py
│       ├── connect.py
│       ├── create_sqlite_tables.py
│       ├── create_tables.py
│       ├── database.ini
│       ├── insert.py
│       ├── insert_demo_user.py
│       ├── models/
│       │   ├── auth_db.py
│       │   ├── db.py
│       │   ├── entities
│       │   └── __init__.py
│       └── instance/
├── requirements.txt
└── Base-de-Datos-Avanzadas/
    ├── README.md
    ├── fake/
    ├── requirements.txt
    └── labo2/
        ├── app.py
        ├── routes/
        │   ├── main.py
        │   ├── alumnos.py
        │   ├── profesores.py
        │   ├── cursos.py
        │   └── matriculas.py
        ├── models/
        │   ├── __init__.py
        │   ├── db.py
        │   ├── entities.py
        │   └── auth_db.py
        ├── templates/
        │   ├── index.html
        │   ├── alumnos.html
        │   ├── alumnos_curso.html
        │   ├── create_alumno.html
        │   ├── cursos.html
        │   ├── cursos_alumno.html
        │   ├── cursos_profesor.html
        │   ├── profesores.html
        │   ├── matriculas.html
        │   ├── create_matricula.html
        │   ├── base.html
        │   └── auth/login.html
        ├── static/
        ├── instance/auth.db
        ├── config.py
        ├── connect.py
        ├── consulta_1_2.py
        ├── create_sqlite_tables.py
        ├── create_tables.py
        ├── delete.py
        ├── fetch_all.py
        ├── fetch_many.py
        ├── fetch_one.py
        ├── insert.py
        ├── insert_demo_data.py
        ├── insert_demo_user.py
        ├── read_blob.py
        ├── transaction.py
        ├── update.py
        ├── write_blob.py
        ├── call_function.py
        ├── call_stored_procedure.py
        ├── database.ini
        └── requirements.txt
```

# Cómo levantar Airflow

En el archivo `airflow/.env`, añadir al final:
```env
_PIP_ADDITIONAL_REQUIREMENTS=psycopg[binary,pool]==3.2.13 Faker==22.6.0
```

# Cómo levantar Airflow
En segundo plano (detached)

```bash
docker compose up -d
```

Con logs en la terminal:
```bash
docker compose up
```

Luego escribir en el navegador: `http://localhost:8080` e iniciar sesión.

# Cómo ejecutar ambos DAGs

1. Los dags deben estar dentro de la carpeta /dags, y reiniciar Airflow en caso no aparezca en la **pestaña de Dags** en el navegador, **la búsqueda se hace por el _id_ del dag**, no por el nombre del fichero.

2. Una vez encontrado los dags, ejecutar **Trigger** para su ejecución. (Primero ejecutar `postgres_pipeline_simple` y luego `dag_de_usuarios`)

# Cómo arrancar la aplicación MVC
```bash
flask run
```
Luego escribir en el navegador: `http://127.0.0.1:5000/` e iniciar sesión.

# Con qué usuario se puede entrar al sistema.

```
admin
profesor
alumno
```



