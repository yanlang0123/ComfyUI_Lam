@echo off
CALL :NORMALIZEPATH "..\..\..\python_embeded\python.exe"
if exist "..\..\..\python_embeded\python.exe" (
    echo Custom Python build of ComfyUI standalone executable detected:
    echo "%RETVAL%"
    echo --------------------------------------------------
    ..\..\..\python_embeded\python.exe changeRestore.py --res %1
) else (
    for /f "tokens=*" %%i in ('where python') do set "PYTHON_PATH=%%i" & goto :done
    :done
    echo Custom Python not found. Use system's Python executable instead:
    echo %PYTHON_PATH%
    echo --------------------------------------------------
    python.exe changeRestore.py --res %1
)

:NORMALIZEPATH
    SET RETVAL=%~f1
    pause

