@echo off
set "_plugin_dir=%~dp0.."

mklink /D "%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ferramentas_pto_controle" "%_plugin_dir%"
