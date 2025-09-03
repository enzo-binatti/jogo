@echo off
echo Instalando Python e Pygame...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Por favor, instale Python manualmente de:
    echo https://www.python.org/downloads/
    echo Lembre-se de marcar "Add Python to PATH" durante a instalação!
    pause
    exit
)

REM Instalar Pygame
pip install pygame

echo.
echo Instalação concluída! Execute o jogo com: python jogo_espacial.py
pause