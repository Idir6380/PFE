from facenet_pytorch import MTCNN
import cv2
from PIL import Image
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm 

# Initialize MTCNN

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# mtcnn = MTCNN(keep_all=True, device=device)


def detect_face(image_path):
    img_cv2 = cv2.imread(image_path)

    # Convert OpenCV image (BGR) to PIL image (RGB)
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # Detect faces
    boxes, _ = mtcnn.detect(img_pil)

    # Draw boxes if faces detected
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img_cv2, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return True
    else:
        return False

    # # Show image with OpenCV
    # cv2.imshow("Face Detection", img_cv2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def show_image(image_path):

    img_cv2 = cv2.imread(image_path)

    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)


    # Show image with OpenCV
    cv2.imshow("Face Detection", img_cv2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


imgs = [f'{i}.jpg' for i in pd.read_csv('./preprocessed.csv')['id'].values]


# Load image with OpenCV

root = "C:\\Users\\DropZone\\OneDrive\\Bureau\\PFE-Gen-AI-TryOn\\DATA\\dataset_annotations\images\\"


# not_face = []

# for img in tqdm(imgs, desc="Detecting face"):
#     if detect_face(root+img) == False:
#         not_face.append(img)
#     else:
#         continue


# with open('/content/not_face.txt', 'w') as f:
#   for nf in not_face:
#     f.write(nf)


to_delete = []
with open('./not_face.txt', 'r') as f:
    for face in f.readlines():
        to_delete.append(face)

to_delete = [td.split('.')[0] for td in to_delete]
print(to_delete)









df = pd.read_csv('./preprocessed.csv')



df = df.drop(df[df['id'].isin(to_delete)].index)



df.to_csv('./preprocessed_2.csv', index=False)