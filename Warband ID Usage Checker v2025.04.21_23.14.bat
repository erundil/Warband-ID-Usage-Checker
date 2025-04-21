::Make sure to give the same name to the *.py file and this *.bat file, then run the *.bat file.
:start
echo off&&cls&&title Warband ID Usage Checker is working...
::get start time
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100")
::execute script
set "PATH=C:\Program Files\Python27;%PATH%"
set "PYTHONPATH=%cd%;%PYTHONPATH%"
python "%~n0.py"
::get end time
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100")
::calculate elapsed time
set /A elapsed=end-start&&set /A cc=elapsed%%100, ss=(elapsed/100)%%60, mm=(elapsed/6000)%%60, hh=elapsed/360000
if %cc% lss 10 set cc=0%cc%
if %mm% gtr 0 if %ss% lss 10 set ss=0%ss%
if %hh% gtr 0 if %mm% lss 10 set mm=0%mm%
::display result
if %hh% equ 0 if %mm% equ 0 title Warband ID Usage Checker have finished in: %ss%.%cc%s
if %hh% equ 0 if %mm% gtr 0 title Warband ID Usage Checker have finished in: %mm%min %ss%.%cc%s
if %hh% gtr 0               title Warband ID Usage Checker have finished in: %hh%h %mm%min %ss%.%cc%s
echo.&&echo ========================================================================================================================&&echo.
::restart variant
echo|set /p temp=Press any key to restart...&&pause>nul&&goto:start
::exit variant
::echo|set /p temp=Press any key to exit...&&pause>nul