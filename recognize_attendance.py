import cv2
import pandas as pd
import os
from datetime import datetime

# ================= CONFIG ================= #
BASE_DIR = os.getcwd()
TRAINER_PATH = os.path.join(BASE_DIR, "trainer", "face_trainer.yml")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

# Build label map safely (sorted for consistency)
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR, exist_ok=True)

LABEL_MAP = sorted([
    name for name in os.listdir(DATASET_DIR)
    if os.path.isdir(os.path.join(DATASET_DIR, name))
])

# ================= RECOGNITION ================= #
def start_recognition():
    if not os.path.exists(TRAINER_PATH):
        print("❌ Model not trained!")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    present_students = set()

    print("🎥 Attendance started. Press Q to finish.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # LBPH: lower confidence = better match
            if confidence < 70 and id_num < len(LABEL_MAP):
                name = LABEL_MAP[id_num]

                # Extra safety
                if name.lower() != "unknown":
                    present_students.add(name)

                color = (0, 255, 0)
                text = f"{name} ({round(100-confidence,1)}%)"

            else:
                text = "Unknown"
                color = (0, 0, 255)

            cv2.putText(
                frame,
                text,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.imshow("Marking Attendance - Press Q to Finish", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ================= SAVE ATTENDANCE ================= #
    if not present_students:
        print("⚠ No valid students detected.")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")

    attendance_dir = os.path.join(BASE_DIR, "attendance")
    os.makedirs(attendance_dir, exist_ok=True)

    file_path = os.path.join(attendance_dir, f"attendance_{date_str}.csv")

    new_data = pd.DataFrame(
        [{"Name": name, "Time": time_str} for name in present_students]
    )

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat(
            [existing_df, new_data]
        ).drop_duplicates(subset="Name", keep="first")
        updated_df.to_csv(file_path, index=False)
    else:
        new_data.to_csv(file_path, index=False)

    print("✅ Attendance saved successfully.")

# ================= RUN ================= #
if __name__ == "__main__":
    start_recognition()
