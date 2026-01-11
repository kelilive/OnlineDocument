mode con cols=50 lines=16 & color 9 & echo off & cls & title dos help document builder

setlocal enabledelayedexpansion

echo ++++++++++ dos help document builder ++++++++++
echo.
echo creating...
echo creating file head...

> dos_help_document.html echo ^<head^>
>> dos_help_document.html echo ^<title^>command help document^</title^>
>> dos_help_document.html echo ^<meta http-equiv="content-type" content="text/htmll^; charset=gb2312" ^/^>
>> dos_help_document.html echo ^</head^>
>> dos_help_document.html echo ^<a name="top"^>
>> dos_help_document.html echo ^<center^>^<h1^>command help document^</h1^>%username% - %date%^</center^>^<br^>
>> dos_help_document.html echo ^<table^>

echo create help category...

for /f "delims=:" %%f in ('help^|findstr /n "^assoc"') do set head=%%f

set /a head-=1

if "%head%" == "0" (set head=) else set head=skip=%head%

for /f "%head% delims=" %%i in ('help') do (
    set str=%%i & set name=!str:~0,9! & set desc=!str:~9!

    echo !name! | findstr /v "^[a-z]" > nul && echo !desc! >> dos_help_document.html

    if errorlevel 1 echo ^</td^>^</tr^>^<tr^>^<td^>^<a href="#!name!"^>!name!^</a^>^</td^>^<td^>!desc! >> dos_help_document.html
)

>> dos_help_document.html echo ^</td^>^</tr^>^</table^>^<br^>^<a href="#top"^>go home^</a^>^<br^>

echo create help content...
echo.

cscript //h:cscript //b

for /f %%i in ('help^|findstr "^[a-z]"') do (
    if /i not "%%i" == "graftabl" (
        >> dos_help_document.html echo ^<a name="%%i"^>^<h2^>[%%i]^</h2^>^<pre^>

        echo creating [%%i] help content...
        help %%i | findstr "<.*>" > nul

        if not errorlevel 1 (
            for /f "delims=" %%a in ('help %%i') do (
                set st=%%a & set st=!st:^<=^<! & set st=!st:^>=^>!
                echo !st!>> dos_help_document.html
            )
        ) else help %%i >> dos_help_document.html
        
        >> dos_help_document.html echo ^</pre^>^<a href="#top"^>go home^</a^>^<br^>^<br^>
    )
)

echo.
echo completed^^!
echo.
echo ++++++++++ dos help document builder ++++++++++

pause > nul && start dos_help_document.html