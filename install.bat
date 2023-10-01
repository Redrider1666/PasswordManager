@echo off

echo Installing librarys...
echo.

pip install mysql.connector tkinter

if %errorlevel% neq 0 (
    echo Error to install the requirements.
    echo Verify if you have python installed in your computer or try to install the requirements manually.
    pause
    exit /b
)

echo All libraries installed successfully.
echo.

echo Starting the program...
echo.

python app.py

pause