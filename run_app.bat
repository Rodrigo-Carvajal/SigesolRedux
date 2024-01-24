@echo off

REM Activar el entorno virtual
..\env\Scripts\activate && (
    REM Ejecutar la aplicación Flask
    python app.py  REM Reemplaza "tu_app.py" por el nombre de tu archivo principal de la aplicación Flask
)
