import cv2
import numpy as np
import os

dataset_path = "dataset"
trainer_path = "trainer/face_trainer.yml"

recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8,
    threshold=80.0
)

faces = []
labels = []
label_map = {}
current_label = 0

print("📚 Reading dataset...")

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    label_map[current_label] = person_name

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if gray_img is None:
            continue

        faces.append(gray_img)
        labels.append(current_label)

    current_label += 1

print("🧠 Training model...")

recognizer.train(faces, np.array(labels))

os.makedirs("trainer", exist_ok=True)
recognizer.save(trainer_path)

print("✅ Model trained successfully")
print("📁 Model saved at:", trainer_path)
print("👤 Label mapping:", label_map)
