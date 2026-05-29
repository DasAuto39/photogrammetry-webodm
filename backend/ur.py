import requests
import time
import cv2
import os
import json
import signal
import sys

global id_frame
id_frame = 0

ESP32_IP = os.getenv("ESP32_IP", "http://192.168.200.219")
SAVE_DIR = "datasets"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# =========================
# KONFIGURASI KAMERA
# =========================
CAMERA_ID = 1

# buka kamera SEKALI
# cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
if not cap.isOpened():
    raise Exception("[ERROR] Kamera gagal dibuka")

# =========================
# SETTING KAMERA
# =========================

# Resolusi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# FPS
cap.set(cv2.CAP_PROP_FPS, 30)

# Gunakan MJPG agar stabil
cap.set(cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*'MJPG'))

# Buffer kecil supaya frame fresh
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#
# =========================
# RESET KE DEFAULT
# =========================

# Autofocus aktif
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

# Auto white balance aktif
cap.set(cv2.CAP_PROP_AUTO_WB, 1)

# Auto exposure aktif
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

print("[INFO] Warmup kamera...")

# warmup kamera
for _ in range(30):
    cap.read()
    time.sleep(0.03)

print("[SUCCESS] Kamera siap")


def set_relay_active(relay_id, state):
    url = f"{ESP32_IP}/relay/{relay_id}"

    try:
        requests.post(url,
                      data={'state': state},
                      timeout=2)
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
    """
    Pengambilan foto yang lebih stabil
    """

    global id_frame

    # =========================
    # BUANG FRAME AWAL
    # =========================
    # penting agar exposure stabil
    for _ in range(5):
        cap.read()

    # ambil beberapa frame
    best_frame = None

    for i in range(5):
        ret, frame = cap.read()

        if ret:
            best_frame = frame

        time.sleep(0.02)

    if best_frame is None:
        print("[ERROR] Gagal capture frame")
        return

    filename = f"{SAVE_DIR}/frame_{id_frame}.jpg"

    # kualitas jpeg tinggi
    cv2.imwrite(
        filename,
        best_frame,
        [cv2.IMWRITE_JPEG_QUALITY, 98]
    )

    print(f"[SUCCESS] Foto disimpan: {filename}")

    id_frame += 1


def main():
    print("Program dimulai...")

    def handle_sigterm(signum, frame):
        print("\n[INFO] Menerima sinyal stop (SIGTERM). Membersihkan kamera...")
        if 'cap' in globals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_sigterm)

    # bersihkan folder
    for f in os.listdir(SAVE_DIR):
        os.remove(os.path.join(SAVE_DIR, f))

    if set_relay_active(0, "on"):
        print("Relay aktif")

    jatah_foto = 1

    try:
        while True:

            inputs = get_input_states()

            if inputs:

                pin_33 = next(
                    (item for item in inputs
                     if item["pin"] == 33),
                    None
                )

                pin_32 = next(
                    (item for item in inputs
                     if item["pin"] == 32),
                    None
                )

                # =========================
                # TRIGGER FOTO
                # =========================
                if pin_33:

                    state_33 = pin_33["state"]

                    if state_33 == 1:

                        if jatah_foto > 0:
                            print("[TRIGGER] Capture")

                            take_photo_opencv()

                            jatah_foto = 0

                    else:

                        if jatah_foto == 0:
                            jatah_foto = 1
                            print("[READY]")

                # =========================
                # STOP
                # =========================
                if pin_32:

                    state_32 = pin_32["state"]

                    if state_32 == 1:

                        print("[INFO] Selesai")

                        set_relay_active(0, "off")

                        break

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgram dihentikan")

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()