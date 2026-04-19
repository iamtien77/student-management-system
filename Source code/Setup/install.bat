@echo off
title Student Management System - Installer & Launcher
color 0B

echo ==========================================================
echo        QUAN LY SINH VIEN (SMS) - INSTALLATION SCRIPT
echo ==========================================================
echo.
echo Xin chao! Truoc khi bat dau, vui long chon moi truong chay:
echo.
echo [1] Chay tren May Tinh hien tai (Khuyen nghi cho Giao dien Tkinter)
echo [2] Chay thong qua Docker (Yeu cau co phan mem X-Server nhu VcXsrv/Xming)
echo [3] Thoat
echo.

set /p choice="Moi ban nhap lua chon (1/2/3): "

if "%choice%"=="1" goto run_local
if "%choice%"=="2" goto run_docker
if "%choice%"=="3" goto exit

:run_local
echo.
echo Bat dau tien trinh khoi tao Virtual Environment (Moi truong ao) python...
cd /d "%~dp0.."
if not exist "venv" (
    echo [*] Dang tao venv moi...
    python -m venv venv
)
echo [*] Kich hoat moi truong ao...
call venv\Scripts\activate.bat
echo [*] Khoi dong chuong trinh SMS...
python Source\main.py
pause
goto exit

:run_docker
echo.
echo [*] Bat dau tien trinh Build ban sao Docker..
cd /d "%~dp0.."
docker build -t student-management-app .
echo.
echo =========================================================================
echo [CANH BAO QUAN TRONG DOCKER WINDOWS]
echo Phan mem nay co giao dien (GUI). Neu ban dung Docker tren Window,
echo ban BAT BUOC phai dang bat mot phan mem X11-Server vi du nhu VcXsrv.
echo Trong VcXsrv, hay chon tick vao o "Disable access control".
echo Dong thoi hay chac chan muc DISPLAY cua ban dang mo port 0.0.
echo =========================================================================
echo An phim bat ky de bat container...
pause > nul
docker run --rm -it -e DISPLAY=host.docker.internal:0.0 student-management-app
pause
goto exit

:exit
exit
