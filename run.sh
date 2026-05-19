#!/bin/bash

echo "Menyalakan venv"
source venv/bin/activate


echo "Memulai NodeODM Docker container di background"
sudo docker run -d -p 3000:3000 opendronemap/nodeodm


sleep 3

echo "Menjalankan Python UI App"
python3 ui/app.py