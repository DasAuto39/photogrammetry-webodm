# Presepsi WebODM

Repository ini berisi skrip dan dataset pendukung untuk menjalankan proses Reconstruction/Structure-from-Motion sederhana.

Terdapat dua cara untuk menjalankan proyek ini:

1. Menggunakan skrip shell (direkomendasikan)

- Perintah: `./run_odm.sh`
- Keterangan: `run_odm.sh` menyiapkan lingkungan dan menjalankan alur CLI secara otomatis. Ini adalah cara yang paling sederhana dan direkomendasikan karena menggabungkan konfigurasi, dependensi, dan penanganan Docker/izin bila diperlukan.

2. Menggunakan Python langsung (alternatif)

- Perintah: `python3 odm.py`
- Keterangan: Menjalankan skrip Python utama secara langsung. Gunakan cara ini bila Anda perlu men-debug atau memodifikasi `odm.py`.

Prasyarat singkat:

- Python 3.x terpasang untuk menjalankan `odm.py`.
- Pastikan skrip `run_odm.sh` memiliki izin eksekusi: `chmod +x run_odm.sh`.
- Jika proyek menggunakan Docker (opsional), jalankan `./run_docker.sh` bila perlu.

Output dan struktur folder penting:

- `images/` : dataset input (subfolder berisi Datasets/).
- `output/` : hasil keluaran proses.
- `sfm_dataset/` : dataset SfM yang dihasilkan.

Dependencies (Python & sistem)

- Dependensi Python utama yang digunakan oleh `odm.py`:
	- `pyodm` (client untuk berinteraksi dengan WebODM/Node)
	- modul bawaan Python: `os`, `pathlib`

- Jika Anda ingin mengelola dependensi Python, gunakan virtual environment (`venv`) agar paket terisolasi dari sistem:

```bash
# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate

# Instal dependensi (opsional: buat file requirements.txt berisi 'pyodm')
pip install pyodm
```

- Jika Anda menggunakan cara CLI (`run_odm.sh`) dan memerlukan utilitas sistem seperti `jq`, jalankan:

```bash
sudo apt update
sudo apt install jq -y
```

Rekomendasi:

- Gunakan `./run_odm.sh` kecuali Anda tahu perlu menjalankan atau memodifikasi `odm.py` langsung. Skrip shell akan mengurangi langkah manual dan mengurangi kemungkinan kesalahan konfigurasi.

Contoh singkat:

```bash
# Jalankan (direkomendasikan)
./run_odm.sh

# Atau jalankan langsung Python (alternatif)
python3 odm.py
```