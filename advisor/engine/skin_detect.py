import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

# Face landmark indices for forehead, left cheek, right cheek
SKIN_POINTS = {"forehead": 151, "left_cheek": 50, "right_cheek": 280}
PATCH = 15  # half-size of each square patch, in pixels


def get_skin_patches(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")

    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as mesh:
        result = mesh.process(rgb)

    if not result.multi_face_landmarks:
        raise ValueError("No face detected")

    landmarks = result.multi_face_landmarks[0].landmark
    patches = {}
    marked = img.copy()

    for name, idx in SKIN_POINTS.items():
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        patches[name] = img[max(y - PATCH, 0): y + PATCH, max(x - PATCH, 0): x + PATCH]
        cv2.rectangle(marked, (x - PATCH, y - PATCH), (x + PATCH, y + PATCH), (0, 255, 0), 2)

    return patches, marked


if __name__ == "__main__":
    patches, marked = get_skin_patches("data/test_images/face1.png")
    cv2.imshow("Skin patches", marked)
    cv2.waitKey(0)
    cv2.destroyAllWindows()