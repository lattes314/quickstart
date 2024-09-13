@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM 1. Define Variables
set "QUICKSTART_DIR=%USERPROFILE%\.quickstart"
set "VENV_DIR=%QUICKSTART_DIR%\.venv"
set "BATCH_FILE=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\quickstart.bat"
set "PATH_CHECK=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps"

REM 2. Create the .quickstart directory if it doesn't exist
if not exist "%QUICKSTART_DIR%" (
    mkdir "%QUICKSTART_DIR%"
    echo Created directory: %QUICKSTART_DIR%
) else (
    echo Directory already exists: %QUICKSTART_DIR%
)

REM 3. Copy all files (python, templates, config) to the .quickstart directory
echo Copying files...
xcopy /E /I /Y ".quickstart" "%QUICKSTART_DIR%"
if errorlevel 1 (
    echo Error copying files.
    exit /b 1
) else (
    echo Files copied successfully.
)

REM 4. Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed. Please install Python 3 and rerun this script.
    pause
    exit /b 1
) else (
    echo Python 3 is installed.
)

REM 5. Create a virtual environment and install Click library
echo Creating virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
) else (
    echo Virtual environment created at %VENV_DIR%
)

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
) else (
    echo Virtual environment activated.
)

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    call deactivate
    exit /b 1
)

echo Installing Libraries library...
python -m pip install click requests
if errorlevel 1 (
    echo Failed to install libraries.
    call deactivate
    exit /b 1
) else (
    echo Libraries installed successfully.
)
call deactivate
echo Virtual environment deactivated.

REM 6. Create quickstart.bat
    echo Creating quickstart.bat in %BATCH_FILE%...
    echo @echo off > "%BATCH_FILE%"
    echo call "%VENV_DIR%\Scripts\activate" >> "%BATCH_FILE%"
    echo python "%QUICKSTART_DIR%\quickstart.py" %%* >> "%BATCH_FILE%"
    echo call deactivate >> "%BATCH_FILE%"
    echo quickstart.bat created successfully.

REM 7. Prompt user to add quickstart.bat to PATH
echo.
echo Do you want to add quickstart.bat to your PATH environment variable? (Y/N)
set /p USER_CHOICE=Enter Y or N: 

if /I "%USER_CHOICE%"=="Y" (
    REM Check if PATH already includes the directory
    echo Checking if %PATH_CHECK% is in your PATH...
    echo %PATH% | find /I "%PATH_CHECK%" >nul 2>&1
    if errorlevel 1 (
        echo %PATH_CHECK% is not in your PATH.
        echo Adding %PATH_CHECK% to your PATH...
        setx PATH "%PATH%;%PATH_CHECK%"
        if errorlevel 1 (
            echo Failed to add to PATH. Please add %PATH_CHECK% to your PATH manually.
        ) else (
            echo Successfully added %PATH_CHECK% to your PATH.
        )
    ) else (
        echo %PATH_CHECK% is already in your PATH.
    )
) else (
    echo Skipping addition of quickstart.bat to PATH.
    echo You can manually add %BATCH_FILE% to your PATH if you wish.
)

REM 8. Final Message
echo.
echo Installation complete - edit and rename the gitlabProfile_example.ini in the .quickstart directory.
if /I "%USER_CHOICE%"=="Y" (
    echo You can now use the 'quickstart' command from any terminal.
) else (
    echo To use the 'quickstart' command, add quickstart.bat to your PATH manually.
)
pause
ENDLOCAL
