import requests
import time
import cv2  # Import OpenCV
import os
from requests_toolbelt import MultipartEncoder 
import json
import piexif # Pastikan library ini sudah di-import di atas

global id_frame
id_frame = 0

# Konfigurasi
ESP32_IP = "http://192.168.200.219" # Sesuaikan dengan IP ESP32 Anda
SAVE_DIR = "datasets"     # Folder penyimpanan foto

# Buat folder jika belum ada
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


import piexif
import random

# def inject_fake_exif(filepath):
#     """Menyuntikkan EXIF metadata dan GPS ke file gambar"""
#     try:
#         exif_dict = {"0th": {}, "Exif": {}, "GPS": {}}
        
#         # 1. Data Kamera (Menggunakan profil drone DJI agar realistis)
#         exif_dict["0th"][piexif.ImageIFD.Make] = b"DJI"
#         exif_dict["0th"][piexif.ImageIFD.Model] = b"FC7303" 
#         exif_dict["Exif"][piexif.ExifIFD.FocalLength] = (45, 10) # Setara 4.5mm
        
#         # 2. Data GPS (Target UTM Zone 49S - Area ITS)
#         # Menambahkan sedikit nilai acak (random) agar koordinat antar foto tidak 100% sama persis, 
#         # karena WebODM bisa error jika semua foto bertumpuk di satu koordinat milimeter yang sama.
#         rand_offset = random.randint(1, 10) 
        
#         # ... (Latitude dan Longitude tetap sama, hanya efek rand_offset-nya yang mengecil) ...

#         # Turunkan simulasi ketinggian kamera menjadi 1 meter (atau 0.5 meter sesuaikan dengan jarak asli kamera ke meja)
#         exif_dict["GPS"][piexif.GPSIFD.GPSAltitudeRef] = 0
#         exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = (1, 1) # Artinya 1 meter
        
#         # Latitude: ~ 7° 16' 55" S
#         exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = b"S"
#         exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = ((7, 1), (16, 1), (5500 + rand_offset, 100))
        
#         # Longitude: ~ 112° 47' 43" E
#         exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = b"E"
#         exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = ((112, 1), (47, 1), (4300 + rand_offset, 100))
         

#         # 3. Eksekusi penyuntikan ke file
#         exif_bytes = piexif.dump(exif_dict)
#         piexif.insert(exif_bytes, filepath)
        
#     except Exception as e:
#         print(f"[ERROR] Gagal menyuntikkan EXIF ke {filepath}: {e}")


WEBODM_URL = "http://localhost:8000"
USERNAME = "faiq_webodm"      # Sesuaikan dengan saat setup WebODM
PASSWORD = "1234qwer" # Sesuaikan dengan saat setup WebODM
PROJECT_ID = 1

# def upload_to_webodm():
#     print(f"[WEBODM] Memulai upload Task ke Project ID {PROJECT_ID}...")
    
#     # 1. Autentikasi / Ambil Token
#     auth_url = f"{WEBODM_URL}/api/token-auth/"
#     try:
#         login_res = requests.post(auth_url, data={'username': USERNAME, 'password': PASSWORD})
#         login_data = login_res.json()
#         token = login_data.get('token')
        
#         if not token:
#             print(f"[ERROR] Gagal login. Response: {login_data}")
#             return
        
#         headers = {'Authorization': f'JWT {token}'}
#     except Exception as e:
#         print(f"[ERROR] Koneksi ke WebODM gagal: {e}")
#         return

#     # 2. Kumpulkan Foto dari Folder
#     image_files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.jpg')]
#     if not image_files:
#         print("[ERROR] Tidak ada foto di folder datasets.")
#         return
    
#     # 3. PROSES PENYUNTIKAN EXIF SEBELUM UPLOAD
#     print(f"[WEBODM] Menyuntikkan EXIF metadata ke {len(image_files)} foto...")
#     for img in image_files:
#         path = os.path.join(SAVE_DIR, img)
#         inject_fake_exif(path)
        
#     print("[SUCCESS] EXIF berhasil disuntikkan ke semua foto.")

#     # Opsi pemrosesan
#    # Opsi pemrosesan disamakan dengan task yang successful
#     options = json.dumps([
#         {"name": "auto-boundary", "value": True},
#         {"name": "mesh-octree-depth", "value": 12},
#         {"name": "use-3dmesh", "value": True},
#         {"name": "pc-quality", "value": "high"},
#         {"name": "mesh-size", "value": 300000}
#     ])

#     fields = [
#         ('name', f'Auto Task dari Python ({len(image_files)} foto)'), # Nama task otomatis
#         ('project', str(PROJECT_ID)),
#         ('options', options)
#     ]
    
#     # Tambahkan gambar
#     opened_files = []
#     for img in image_files:
#         path = os.path.join(SAVE_DIR, img)
#         f = open(path, 'rb')
#         opened_files.append(f)
#         fields.append(('images', (img, f, 'image/jpeg')))

#     # 3. Upload & Mulai Task
#     print(f"[WEBODM] Mengunggah {len(image_files)} foto...")
#     m = MultipartEncoder(fields=fields)
#     headers['Content-Type'] = m.content_type

#     # Perhatikan URL-nya, kita langsung tembak ke /tasks/ di dalam project ID
#     task_res = requests.post(
#         f"{WEBODM_URL}/api/projects/{PROJECT_ID}/tasks/",
#         data=m,
#         headers=headers
#     )

#     for f in opened_files:
#         f.close()

#     if task_res.status_code == 201:
#         print("[SUCCESS] Task berhasil ditambahkan ke Project!")
#         print(f"Silakan cek di: {WEBODM_URL}/dashboard/projects/{PROJECT_ID}")
#     else:
#         print(f"[ERROR] Gagal membuat Task ({task_res.status_code}): {task_res.text}")

def set_relay_active(relay_id, state):
    url = f"{ESP32_IP}/relay/{relay_id}"
    try:
        requests.post(url, data={'state': state}, timeout=2)
        return True
    except:
        return False

def get_input_states():
    url = f"{ESP32_IP}/input"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()['inputs']
    except:
        return None

def take_photo_opencv():
    """Fungsi untuk mengambil gambar menggunakan OpenCV"""
    # Inisialisasi kamera (0 adalah kamera default)
    cap = cv2.VideoCapture(3)
    
    if not cap.isOpened():
        print("[ERROR] Tidak dapat mengakses kamera")
        return

    # Beri waktu kamera untuk auto-focus/exposure
    # time.sleep(0.5) 
    
    ret, frame = cap.read()
    if ret:
        global id_frame
        filename = f"{SAVE_DIR}/frame_{id_frame}.jpg"
        id_frame += 1   
        cv2.imwrite(filename, frame)
        print(f"[SUCCESS] Frame disimpan sebagai: {filename}")
    else:
        print("[ERROR] Gagal mengambil gambar dari buffer")

    # Lepas kamera agar bisa digunakan aplikasi lain nanti
    cap.release()

def main():
    print("Program Kontrol ESP32 + OpenCV dimulai...")
    
    # bersihkan folder datasets sebelum mulai
    for f in os.listdir(SAVE_DIR):
        os.remove(os.path.join(SAVE_DIR, f))

    # 1. Set relay 1 (index 0) aktif
    if set_relay_active(0, "on"):
        print("Relay 1 Aktif.")
    
    jatah_foto = 1  
    # take_photo_opencv()  # Ambil foto pertama saat program mulai
    # jatah_foto = 1  # Habiskan jatah pertama

    try:
        while True:
            global id_frame
            # upload_to_webodm()  # Cek setiap loop apakah sudah mencapai 30 frame
            # break
            # if id_frame >= 30:
            #     print("[INFO] Sudah mengambil 30 frame, berhenti.")
            #     set_relay_active(0, "off")
            #     upload_to_webodm()
            #     break
            inputs = get_input_states()
            
            if inputs:
                pin_33 = next((item for item in inputs if item["pin"] == 33), None)
                pin_32 = next((item for item in inputs if item["pin"] == 32), None)
                if pin_33:
                    state_33 = pin_33["state"]

                    # 3. Jika Pin 33 Aktif & Ada Jatah
                    if state_33 == 1:
                        if jatah_foto > 0:
                            print("[TRIGGER] Mencoba mengambil foto...")
                            take_photo_opencv()
                            jatah_foto = 0 # Habiskan jatah
                    
                    # 4. Jika Pin 33 Off, Reset Jatah
                    else:
                        if jatah_foto == 0:
                            jatah_foto = 1
                            print("[READY] Pin 33 OFF. Jatah foto dikembalikan.")
                if pin_32:
                    state_32 = pin_32["state"]
                    if state_32 == 1:
                        print("[TRIGGER] Pin 32 ON. Gerakan Selelai. Siap upload ke WebODM...")
                        set_relay_active(0, "off")
                        # upload_to_webodm()
                        break

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()