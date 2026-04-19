#!/bin/bash
# Script Setup & Run hệ thống Quản lý Sinh viên (SMS) cho Linux / macOS

echo "=========================================================="
echo "      QUAN LY SINH VIEN (SMS) - INSTALLATION SCRIPT       "
echo "=========================================================="
echo ""
echo "Xin chao! Truoc khi bat dau, vui long chon moi truong chay:"
echo ""
echo "[1] Chay tren May Tinh hien tai (Local - Khuyen nghi)"
echo "[2] Chay thong qua Docker (Yeu cau cau hinh X11 Server)"
echo "[3] Thoat"
echo ""

read -p "Moi ban nhap lua chon (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "[*] Bat dau tien trinh khoi tao Virtual Environment (Moi truong ao)..."
        cd "$(dirname "$0")/.."
        if [ ! -d "venv" ]; then
            echo "[*] Dang tao venv moi..."
            python3 -m venv venv
        fi
        echo "[*] Kich hoat moi truong ao..."
        source venv/bin/activate
        echo "[*] Khoi dong chuong trinh SMS..."
        python3 Source/main.py
        ;;
    2)
        echo ""
        echo "[*] Bat dau tien trinh Build ban sao Docker..."
        cd "$(dirname "$0")/.."
        docker build -t student-management-app .
        echo ""
        echo "========================================================================="
        echo "[CANH BAO QUAN TRONG CHO DOCKER TRUNG GIAN]"
        echo "Neu ban xai Linux, ban se can day lenh 'xhost +local:docker' hoac tuong tu"
        echo "de cap quyen cho Container ban tin hieu hinh anh Tkinter ra Desktop."
        echo "Voi MacOS, hay chac chan ban da dung XQuartz va option 'Allow connections'"
        echo "========================================================================="
        read -p "An Enter bat ky de tiep tuc chay Docker..."
        
        # Mapping X11 Socket Unix de in giao dien trong Linux - Mac
        docker run --rm -it \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            student-management-app
        ;;
    *)
        echo "Thoat chuong trinh..."
        exit 0
        ;;
esac
