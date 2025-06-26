import cv2
import pickle
import numpy as np
import cvzone
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os

Tk().withdraw()

video_path = askopenfilename(
    title="Pilih video parkiran",
    filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
)

if not video_path:
    print("Tidak ada video yang dipilih.")
    exit()

with open("selected_video.txt", "w") as f:
    f.write(video_path)

def get_pos_filename(video_path):
    base_name = os.path.basename(video_path)
    name, _ = os.path.splitext(base_name)
    return f"static/coordinate/CarParkPos_{name}.pkl"

posList = []
currentBox = []

pos_file = get_pos_filename(video_path)

if os.path.exists(pos_file):
    response = messagebox.askyesno(
        "Koordinat Ditemukan",
        "Koordinat sudah tersedia untuk video ini.\nApakah Anda ingin menandai ulang?"
    )

    if response:
        posList = []
        print("[INFO] Tandai ulang koordinat parkir.")

        def mouseClick(event, x, y, flags, param):
            global currentBox
            if event == cv2.EVENT_LBUTTONDOWN:
                currentBox.append((x, y))
                print(f"Titik {len(currentBox)}: {x}, {y}")

                if len(currentBox) == 4:
                    posList.append(currentBox.copy())
                    print(f"Tambah kotak: {currentBox}")
                    currentBox = []

        cap = cv2.VideoCapture(video_path)
        success, img = cap.read()
        cap.release()

        if not success:
            print("Gagal membaca video.")
            exit()

        cv2.namedWindow("Tandai Kotak")
        cv2.setMouseCallback("Tandai Kotak", mouseClick)

        while True:
            img_copy = img.copy()

            for box in posList:
                pts = cv2.convexHull(np.array(box, dtype=np.int32))
                cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            for pt in currentBox:
                cv2.circle(img_copy, pt, 5, (255, 0, 0), cv2.FILLED)

            cv2.imshow("Tandai Kotak", img_copy)
            key = cv2.waitKey(1)

            if key == ord('s'):
                with open(pos_file, 'wb') as f:
                    pickle.dump(posList, f)
                print(f"✅ Semua kotak disimpan ke '{pos_file}'")

            elif key == ord('q'):
                print("🔄 Menjalankan video dengan koordinat yang ditandai...")
                break

        cv2.destroyAllWindows()
    else:
        print(f"[INFO] Menggunakan koordinat dari file {pos_file}")
        with open(pos_file, "rb") as f:
            posList = pickle.load(f)
else:
    print("[INFO] Belum ada koordinat, silakan tandai kotak dulu.")

    def mouseClick(event, x, y, flags, param):
        global currentBox
        if event == cv2.EVENT_LBUTTONDOWN:
            currentBox.append((x, y))
            print(f"Titik {len(currentBox)}: {x}, {y}")

            if len(currentBox) == 4:
                posList.append(currentBox.copy())
                print(f"Tambah kotak: {currentBox}")
                currentBox = []

    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    cap.release()

    if not success:
        print("Gagal membaca video.")
        exit()

    cv2.namedWindow("Tandai Kotak")
    cv2.setMouseCallback("Tandai Kotak", mouseClick)

    while True:
        img_copy = img.copy()

        for box in posList:
            pts = cv2.convexHull(np.array(box, dtype=np.int32))
            cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        for pt in currentBox:
            cv2.circle(img_copy, pt, 5, (255, 0, 0), cv2.FILLED)

        cv2.imshow("Tandai Kotak", img_copy)
        key = cv2.waitKey(1)

        if key == ord('s'):
            with open(pos_file, 'wb') as f:
                pickle.dump(posList, f)
            print(f"✅ Semua kotak disimpan ke '{pos_file}'")

        elif key == ord('q'):
            print("🔄 Menjalankan video dengan koordinat yang ditandai...")
            break

    cv2.destroyAllWindows()

# === FUNGSI CHECK PARKING SPACE YANG DIPAKAI DI VIDEO ===
def checkParkingSpace(imgPro, img, posList, threshold=900):
    spaceCounter = 0

    for box in posList:
        pts = np.array(box, np.int32)
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect

        roi_cropped = imgPro[y:y + h, x:x + w]
        pts_shifted = pts - [x, y]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [pts_shifted], 255)
        parking_area = cv2.bitwise_and(roi_cropped, roi_cropped, mask=mask)
        count = cv2.countNonZero(parking_area)

        if count < threshold:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.polylines(img, [pts], isClosed=True, color=color, thickness=thickness)
        cvzone.putTextRect(img, str(count), tuple(pts[0]), scale=1, thickness=1, offset=1, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


# === TAMPILKAN VIDEO DENGAN DETEKSI ===
def nothing(x):
    pass

def play_video_with_detection(video_path, pos_file):
    with open(pos_file, "rb") as f:
        posList = pickle.load(f)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Tidak bisa membuka video.")
        return

    # Buat jendela dan trackbar
    cv2.namedWindow("Deteksi Parkiran")
    cv2.createTrackbar("Threshold", "Deteksi Parkiran", 2, 10, nothing)  # Default 1000

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        if not success:
            break

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(
            imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        # Ambil nilai threshold dari trackbar
        # threshold_val = cv2.getTrackbarPos("Threshold", "Deteksi Parkiran")
        threshold_multiplier = cv2.getTrackbarPos("Threshold", "Deteksi Parkiran")
        threshold_val = threshold_multiplier * 500

        checkParkingSpace(imgDilate, img, posList, threshold=threshold_val)

        cv2.imshow("Deteksi Parkiran", img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Jalankan video setelah selesai menandai
if os.path.exists(pos_file):
    play_video_with_detection(video_path, pos_file)
