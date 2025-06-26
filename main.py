from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import pickle
import numpy as np
import cvzone
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
COORD_FOLDER = "static/coordinate"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COORD_FOLDER, exist_ok=True)

def checkParkingSpace(imgPro, img, posList, threshold=900):
    spaceCounter = 0
    for box in posList:
        pts = np.array(box, np.int32)
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect

        if y + h > imgPro.shape[0] or x + w > imgPro.shape[1]:
            continue

        roi_cropped = imgPro[y:y + h, x:x + w]
        pts_shifted = pts - [x, y]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [pts_shifted], 255)

        if roi_cropped.shape != mask.shape:
            continue

        parking_area = cv2.bitwise_and(roi_cropped, roi_cropped, mask=mask)
        count = cv2.countNonZero(parking_area)

        color = (0, 255, 0) if count < threshold else (0, 0, 255)
        thickness = 5 if count < threshold else 2
        if count < threshold:
            spaceCounter += 1

        cv2.polylines(img, [pts], isClosed=True, color=color, thickness=thickness)
        cvzone.putTextRect(img, str(count), tuple(pts[0]), scale=1, thickness=1, offset=1, colorR=color)

    cvzone.putTextRect(
        img, f'Free: {spaceCounter}/{len(posList)}', (50, 50),
        scale=3, thickness=3, offset=10, colorR=(0, 200, 0)
    )
    
def create_coordinates_with_mouse(video_path, coord_path):
    posList = []
    currentBox = []

    def mouseClick(event, x, y, flags, param):
        nonlocal currentBox
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
        return

    cv2.namedWindow("Tandai Slot Parkir (Tekan S untuk Simpan, Q untuk Keluar)")
    cv2.setMouseCallback("Tandai Slot Parkir (Tekan S untuk Simpan, Q untuk Keluar)", mouseClick)

    while True:
        img_copy = img.copy()
        for box in posList:
            pts = cv2.convexHull(np.array(box, dtype=np.int32))
            cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        for pt in currentBox:
            cv2.circle(img_copy, pt, 5, (255, 0, 0), cv2.FILLED)

        cv2.imshow("Tandai Slot Parkir (Tekan S untuk Simpan, Q untuk Keluar)", img_copy)
        key = cv2.waitKey(1)
        if key == ord('s'):
            with open(coord_path, 'wb') as f:
                pickle.dump(posList, f)
            print(f"✅ Koordinat disimpan ke {coord_path}")
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

def generate(path, threshold, video_filename):
    base_name = os.path.splitext(os.path.basename(video_filename))[0]
    coord_path = os.path.join(COORD_FOLDER, f"CarParkPos_{base_name}.pkl")

    if not os.path.exists(coord_path):
        print(f"[INFO] Koordinat belum tersedia. Silakan tandai dulu.")
        create_coordinates_with_mouse(path, coord_path)

    with open(coord_path, "rb") as f:
        posList = pickle.load(f)

    cap = cv2.VideoCapture(path)
    while True:
        success, img = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(
            imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkParkingSpace(imgDilate, img, posList, threshold=threshold)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    threshold = request.args.get('threshold', type=int)
    video_filename = request.args.get('video_filename', type=str)
    video_ready = False
    coord_exists = False

    if video_filename:
        video_path = os.path.join(UPLOAD_FOLDER, video_filename)
        base_name = os.path.splitext(video_filename)[0]
        coord_path = os.path.join(COORD_FOLDER, f"CarParkPos_{base_name}.pkl")
        coord_exists = os.path.exists(coord_path)
        video_ready = os.path.exists(video_path) and coord_exists

    return render_template('index.html',
                           threshold=threshold,
                           video_ready=video_ready,
                           video_filename=video_filename,
                           coord_exists=coord_exists)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "Tidak ada video", 400

    file = request.files['video']
    if file.filename == '':
        return "File tidak dipilih", 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    return redirect(url_for('index', video_filename=filename, threshold=900))

@app.route('/video_feed')
def video_feed():
    threshold = request.args.get('threshold', default=900, type=int)
    filename = request.args.get('video_filename')

    if not filename:
        return "Video tidak ditemukan", 400

    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(video_path):
        return "Video tidak ditemukan", 404

    return Response(generate(video_path, threshold, filename),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
