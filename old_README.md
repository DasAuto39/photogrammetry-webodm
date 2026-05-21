# Presepsi WebODM

Repository ini berisi skrip dan dataset pendukung untuk menjalankan proses Reconstruction/Structure-from-Motion sederhana.

Terdapat dua cara untuk menjalankan proyek ini:

1. Menggunakan skrip shell (direkomendasikan)

- Perintah: `./run_odm.sh`
- Keterangan: `run_odm.sh` menyiapkan lingkungan dan menjalankan alur CLI secara otomatis. Ini adalah cara yang paling sederhana dan direkomendasikan karena menggabungkan konfigurasi, dependensi, dan penanganan Docker/izin bila diperlukan.

2. Menggunakan Python langsung (alternatif)

- Perintah: `python3 odm.py`
- Keterangan: Menjalankan skrip Python utama secara langsung. Gunakan cara ini bila Anda perlu men-debug atau memodifikasi `odm.py`.

3. Menjalankan `ur.py` secara terpisah (capture via ESP32 + kamera)

- Perintah: `python3 ur.py`
- Keterangan: `ur.py` digunakan untuk kontrol relay/input ESP32 dan pengambilan gambar kamera (OpenCV), terpisah dari alur `odm.py`.

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

- Dependensi Python untuk `ur.py`:
	- `requests`
	- `requests-toolbelt`
	- `opencv-python`
	- `piexif`
	- modul bawaan Python: `time`, `os`, `json`, `random`

- Jika Anda ingin mengelola dependensi Python, gunakan virtual environment (`venv`) agar paket terisolasi dari sistem:

```bash
# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate

# Instal dependensi untuk odm.py
pip install pyodm

# Instal dependensi untuk ur.py (terpisah)
pip install requests requests-toolbelt opencv-python piexif

# Atau instal semua sekaligus
pip install pyodm requests requests-toolbelt opencv-python piexif
```

Catatan untuk `ur.py`:

- Pastikan nilai `ESP32_IP` di [ur.py](ur.py) sesuai IP perangkat ESP32 Anda.
- Di Linux, jika OpenCV gagal membuka kamera, pastikan device kamera terdeteksi (mis. `/dev/video*`) dan user punya izin akses.

- Jika Anda menggunakan cara CLI (`run_odm.sh`) dan memerlukan utilitas sistem seperti `jq`, jalankan:

```bash
sudo apt update
sudo apt install jq -y
```

## Docker - NodeODM Setup (Opsional)

Jika Anda ingin menggunakan WebODM dengan NodeODM di dalam Docker, gunakan image Docker resmi dari OpenDroneMap:

**Dokumentasi**: https://hub.docker.com/r/opendronemap/nodeodm

### Quick Start dengan Docker

Pull dan jalankan NodeODM dari Docker Hub:

```bash
docker run -p 3000:3000 opendronemap/nodeodm
```

Kemudian buka browser ke `http://localhost:3000`

### Dengan Volume External (untuk menyimpan hasil di drive eksternal)

```bash
docker run -p 3000:3000 -v /mnt/external_hd:/var/www/data opendronemap/nodeodm
```

### Dengan GPU Acceleration (untuk NVIDIA GPU)

Jika Anda memiliki GPU NVIDIA, gunakan image GPU:

```bash
docker run -p 3000:3000 --gpus all opendronemap/nodeodm:gpu
```

Pastikan Anda sudah menginstall `nvidia-docker` sebelumnya. Lihat: https://github.com/NVIDIA/nvidia-docker

### Catatan CPU Requirements

Docker images memerlukan CPU 64-bit dengan dukungan MMX, SSE, SSE2, SSE3, dan SSSE3. CPU yang terlalu lama tidak akan kompatibel.

Rekomendasi:

- Gunakan `./run_odm.sh` kecuali Anda tahu perlu menjalankan atau memodifikasi `odm.py` langsung. Skrip shell akan mengurangi langkah manual dan mengurangi kemungkinan kesalahan konfigurasi.

Contoh singkat:

```bash
# Jalankan (direkomendasikan)
./run_odm.sh

# Atau jalankan langsung Python (alternatif)
python3 odm.py
```
jalankan code dibawah untuk ui
```py
	# aktifkan virtualenv Anda jika perlu, lalu:
	pip install -r ui/requirements.txt
	python3 ui/app.py
```

## Web UI End-to-End

Jika Anda ingin alur yang lebih user-friendly berbasis web, gunakan dashboard di `ui/`:

```bash
pip install -r ui/requirements.txt
python3 ui/app.py
```

Lalu buka `http://localhost:5000`.

Urutan pakai yang disarankan:

- Klik `Run All` untuk menjalankan `ur.py` lalu otomatis lanjut `run_odm.sh`.
- Pantau status robot, ODM, dan log proses langsung dari browser.
- Pilih hasil model dari folder `output/output_*/odm_texturing/` dan klik `Load Model`.

## Quick Setup (recommended)

Use these quick steps to prepare a machine for running the end-to-end demo (robot capture → ODM → web UI).

1) Install system utilities (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install -y curl jq git docker.io docker-compose build-essential pkg-config
# allow non-root docker usage (log out/login required)
sudo usermod -aG docker $USER
```

2) (Optional) Run NodeODM in Docker (provides NodeODM on port 3000):

```bash
# Pull and run NodeODM (single command, map port 3000)
docker run -p 3000:3000 opendronemap/nodeodm
```

3) Create Python virtualenv and install Python deps (UI + scripts):

```bash
# from project root
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# UI dependencies
pip install -r ui/requirements.txt
# Script dependencies (ur.py, odm.py)
pip install pyodm requests requests-toolbelt opencv-python piexif
```

4) Camera permissions (if using a local USB camera):

```bash
# allow current user to access /dev/video* devices
sudo usermod -aG video $USER
# then re-login or run new shell
```

5) Make helper scripts executable and run them:

```bash
chmod +x run_odm.sh
# Start the web UI dashboard (browse to http://localhost:5000)
python3 ui/app.py

# or run CLI flow manually:
./run_all.sh    # runs ur.py then run_odm.sh
```

6) Quick troubleshooting

- If buttons in the web UI do not start processes, test endpoints with `curl -v -X POST http://127.0.0.1:5000/api/run_all` and check `output/ui_logs/` for logs.
- If OpenCV can't open the camera, verify `/dev/video*` exists and try `cheese` or `v4l2-ctl --list-devices`.
- If model loading is slow in the browser, prefer converting `.obj` to `.glb` for faster transfer and parsing.
- Ensure Docker is running (systemd), and NodeODM port `3000` is reachable if using Docker.

If you want, I can add a small script that auto-creates the venv and installs the needed packages.