import cv2
import os

# Relative path to haarcascade
cascade_path = os.path.join(os.getcwd(), "haarcascade_frontalface_default.xml")

face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print("❌ Haarcascade file not loaded")
    exit()

# Input person name
person_name = input("Enter person name: ").strip()

dataset_path = os.path.join("dataset", person_name)
os.makedirs(dataset_path, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0
MAX_IMAGES = 50

print("📸 Capturing images...")
print("Press 'q' to quit early")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        img_path = os.path.join(dataset_path, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Image {count}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Collecting Faces", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if count >= MAX_IMAGES:
        break

cap.release()
cv2.destroyAllWindows()

print(f"✅ {count} images saved in dataset/{person_name}")
