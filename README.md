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