@echo off

:LOOP
REM Verificar si la aplicación está en ejecución
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq app.py" | find "python.exe" > nul

IF %ERRORLEVEL% NEQ 0 (
    echo La aplicación no está en ejecución. Iniciando la aplicación...

    REM Detener procesos de Python (opcional)
    taskkill /F /IM python.exe /T > nul

    REM Llamar al script para correr la aplicación Flask
    call run_app.bat
)

REM Esperar 15 segundos antes de volver a verificar
timeout /nobreak /t 5 > nul
goto LOOP
