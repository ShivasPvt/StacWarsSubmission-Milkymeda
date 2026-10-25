@echo off
cd /d "%~dp0"

rem ---- find a real Python (Anaconda first, then the py launcher) ----
set PY=
for %%P in (
  "%USERPROFILE%\anaconda3\python.exe"
  "%USERPROFILE%\miniconda3\python.exe"
  "%LOCALAPPDATA%\anaconda3\python.exe"
  "%LOCALAPPDATA%\miniconda3\python.exe"
  "C:\ProgramData\anaconda3\python.exe"
  "C:\ProgramData\miniconda3\python.exe"
  "C:\anaconda3\python.exe"
) do if not defined PY if exist %%P set PY=%%P

if not defined PY (
  py -3 --version >nul 2>&1 && set PY=py -3
)

if not defined PY (
  echo Could not find Python on this computer.
  echo Open "Anaconda Prompt" from the Start menu, go to this folder and run:
  echo     python stac_ps3.py
  echo     python check_answers.py
  echo     python plot_graphs.py
  pause
  exit /b
)

echo Using Python: %PY%
echo.
echo Installing matplotlib (needed for the graph)...
%PY% -m pip install matplotlib --quiet
echo.
echo ===== 1) Calculations =====
%PY% stac_ps3.py
echo.
echo ===== 2) Tests =====
%PY% check_answers.py
echo.
echo ===== 3) Graph (a window will open, close it to finish) =====
%PY% plot_graphs.py
echo.
echo Done. The graph is also saved as light_curves.png in this folder.
pause
