#!/bin/bash

# Jalankan python terlebih dahulu
python3 ur.py

# Cek apakah python berhasil
if [ $? -eq 0 ]; then
    echo "Python selesai"

    # Jalankan shell script kedua
    ./run_odm.sh datasets/
else
    echo "Python gagal"
fi