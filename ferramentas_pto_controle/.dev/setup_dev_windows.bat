@echo off
REM Liga o plugin deste repositorio ao perfil do QGIS, para desenvolver sem copiar
REM arquivo. O perfil e o QGIS4: o plugin declara qgisMinimumVersion=4.0, e apontar
REM para o QGIS3 legado instala o plugin onde o QGIS 4 nao olha.
REM Precisa de Modo de Desenvolvedor ligado, ou de um terminal como Administrador.
set "_plugin_dir=%~dp0.."
set "_dest=%APPDATA%\QGIS\QGIS4\profiles\default\python\plugins\ferramentas_pto_controle"

if exist "%_dest%" rmdir "%_dest%"
mklink /D "%_dest%" "%_plugin_dir%"
if errorlevel 1 (
    echo.
    echo Falhou o link. Rode como Administrador, ou ligue o Modo de Desenvolvedor.
    exit /b 1
)

echo.
echo Plugin ligado. Falta habilita-lo PARA O qgis_process, que e uma habilitacao
echo separada da do QGIS Desktop:
echo     python "%_plugin_dir%\pto_controle_cli\pto_controle_cli.py" doctor --fix
