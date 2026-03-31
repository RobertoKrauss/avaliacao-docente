@echo off
set BASE=%~dp0
cd /d %BASE%
if exist AvaliacaoDocente.exe (
  AvaliacaoDocente.exe
) else (
  echo Executavel nao encontrado. Gere primeiro com PyInstaller.
)
