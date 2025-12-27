# gen_embeddings.py（只在本地跑）
import os
import numpy as np
from deepface import DeepFace

BASE = "photos"
embeddings = {}

for member in os.listdir(BASE):
    member_dir = os.path.join(BASE, member)
    if not os.path.isdir(member_dir):
        continue

    embs = []
    for img in os.listdir(member_dir):
        path = os.path.join(member_dir, img)
        rep = DeepFace.represent(
            img_path=path,
            model_name="Facenet",
            enforce_detection=False
        )[0]["embedding"]
        embs.append(rep)

    embeddings[member] = np.mean(embs, axis=0)

np.save("ive_embeddings.npy", embeddings)
