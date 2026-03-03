# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import numpy as np
# import io
# import os
# import shutil
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# import joblib

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# # -----------------------
# # Eye Cataract Model
# # -----------------------


# # -----------------------
# # Hybrid TB Model
# # -----------------------

# # -----------------------
# # Eye Cataract Model
# # -----------------------
# eye_model = load_model("model_cataract.keras")
# eye_class_names = ["cataract", "normal"]

# # -----------------------
# # Hybrid TB Model
# # -----------------------
# tb_model = load_model("hybrid_tb_model.keras")
# tb_scaler = joblib.load("meta_scaler.pkl")
# IMG_SIZE_TB = 128

# # -----------------------
# # Routes
# # -----------------------

# @app.post("/predict/eye")
# async def predict_eye(file: UploadFile = File(...)):
#     image_bytes = await file.read()

#     img = load_img(io.BytesIO(image_bytes), target_size=(224, 224), color_mode="rgb")
#     img_array = img_to_array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     pred_probs = eye_model.predict(img_array)[0]
#     pred_idx = int(np.argmax(pred_probs))
#     predicted_class = eye_class_names[pred_idx]
#     confidence = float(pred_probs[pred_idx])

#     return {
#         "class": predicted_class,
#         "confidence": round(confidence, 4)
#     }


# @app.post("/predict/tb")
# async def predict_tb(
#     file: UploadFile = File(...),
#     age: float = Form(...),
    
#     gender: str = Form(...)
# ):
#     # Save uploaded image temporarily
#     temp_path = f"temp_{file.filename}"
#     with open(temp_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Preprocess image (grayscale for TB model)
#     img = load_img(temp_path, color_mode="grayscale", target_size=(IMG_SIZE_TB, IMG_SIZE_TB))
#     img_arr = img_to_array(img) / 255.0
#     img_arr = np.expand_dims(img_arr, axis=0)  # (1,128,128,1)

#     # Preprocess metadata
#     gender_val = 1.0 if gender.lower() in ["m", "male"] else 0.0
#     meta_arr = np.array([[age, gender_val]], dtype=np.float32)
#     meta_arr = tb_scaler.transform(meta_arr)

#     # Predict
#     prob = float(tb_model.predict([img_arr, meta_arr])[0][0])
#     label = "TB" if prob > 0.5 else "Normal"

#     # Clean up temp file
#     os.remove(temp_path)

#     return {
#         "class": label,
#         "confidence": round(prob, 4)
#     }

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import io
import os
import shutil
import gdown
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# GOOGLE DRIVE DOWNLOAD FUNCTION
# -------------------------------------------------

def download_file(file_id, output_path):
    if not os.path.exists(output_path):
        if not file_id:
            raise ValueError(f"{output_path} ID not set in environment")

        print(f"Downloading {output_path} from Google Drive...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output_path, quiet=False)
        print(f"{output_path} downloaded successfully.")


# -------------------------------------------------
# ENVIRONMENT VARIABLES (SET THESE IN RENDER)
# -------------------------------------------------

EYE_MODEL_ID   = os.getenv("EYE_MODEL_ID")
TB_MODEL_ID    = os.getenv("TB_MODEL_ID")
SCALER_ID      = os.getenv("SCALER_ID")

# -------------------------------------------------
# DOWNLOAD FILES IF NOT PRESENT
# -------------------------------------------------

# # download_file(EYE_MODEL_ID, "model_cataract.keras")
# # download_file(TB_MODEL_ID, "hybrid_tb_model.keras")
# download_file(SCALER_ID, "meta_scaler.pkl")

# # -------------------------------------------------
# # LOAD MODELS
# # -------------------------------------------------

# # eye_model = load_model("model_cataract.keras")
# eye_class_names = ["cataract", "normal"]

# # tb_model = load_model("hybrid_tb_model.keras")
# tb_scaler = joblib.load("meta_scaler.pkl")

# IMG_SIZE_TB = 128

# print("All models loaded successfully.")

# -------------------------------------------------
# DOWNLOAD FILES IF NOT PRESENT
# -------------------------------------------------

download_file(EYE_MODEL_ID, "model_cataract_fixed.h5")
download_file(TB_MODEL_ID, "hybrid_tb_model_fixed.h5")
download_file(SCALER_ID, "meta_scaler.pkl")

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------

eye_model = load_model("model_cataract_fixed.h5")
eye_class_names = ["cataract", "normal"]

tb_model = load_model("hybrid_tb_model_fixed.h5")
tb_scaler = joblib.load("meta_scaler.pkl")

IMG_SIZE_TB = 128

print("All models loaded successfully.")

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@app.post("/predict/eye")
async def predict_eye(file: UploadFile = File(...)):
    image_bytes = await file.read()

    img = load_img(io.BytesIO(image_bytes), target_size=(224, 224), color_mode="rgb")
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred_probs = eye_model.predict(img_array)[0]
    pred_idx = int(np.argmax(pred_probs))
    predicted_class = eye_class_names[pred_idx]
    confidence = float(pred_probs[pred_idx])

    return {
        "class": predicted_class,
        "confidence": round(confidence, 4)
    }


@app.post("/predict/tb")
async def predict_tb(
    file: UploadFile = File(...),
    age: float = Form(...),
    gender: str = Form(...)
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = load_img(temp_path, color_mode="grayscale", target_size=(IMG_SIZE_TB, IMG_SIZE_TB))
    img_arr = img_to_array(img) / 255.0
    img_arr = np.expand_dims(img_arr, axis=0)

    gender_val = 1.0 if gender.lower() in ["m", "male"] else 0.0
    meta_arr = np.array([[age, gender_val]], dtype=np.float32)
    meta_arr = tb_scaler.transform(meta_arr)

    prob = float(tb_model.predict([img_arr, meta_arr])[0][0])
    label = "TB" if prob > 0.5 else "Normal"

    os.remove(temp_path)

    return {
        "class": label,
        "confidence": round(prob, 4)
    }