from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import joblib
import io
import tensorflow.lite as tflite

# ===================================================
# APP INIT
# ===================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================================
# GLOBAL VARIABLES
# ===================================================

tb_interpreter = None
kidney_interpreter = None
retina_interpreter = None
skin_interpreter = None
chest14_interpreter = None
scaler = None

# ===================================================
# MODEL LOADERS
# ===================================================

def load_tb_model():
    global tb_interpreter, tb_input_details, tb_output_details

    if tb_interpreter is None:
        print("Loading TB model...")
        tb_interpreter = tflite.Interpreter(model_path="./model_Chest_Tuber.tflite")
        tb_interpreter.allocate_tensors()

        tb_input_details = tb_interpreter.get_input_details()
        tb_output_details = tb_interpreter.get_output_details()

        print("✅ TB model loaded")


def load_kidney_model():
    global kidney_interpreter, kidney_input_details, kidney_output_details

    if kidney_interpreter is None:
        print("Loading Kidney model...")
        kidney_interpreter = tflite.Interpreter(model_path="./kidney_model.tflite")
        kidney_interpreter.allocate_tensors()

        kidney_input_details = kidney_interpreter.get_input_details()
        kidney_output_details = kidney_interpreter.get_output_details()

        print("✅ Kidney model loaded")


def load_retina_model():
    global retina_interpreter, retina_input_details, retina_output_details

    if retina_interpreter is None:
        print("Loading Retina model...")
        retina_interpreter = tflite.Interpreter(model_path="./retinal_fundus.tflite")
        retina_interpreter.allocate_tensors()

        retina_input_details = retina_interpreter.get_input_details()
        retina_output_details = retina_interpreter.get_output_details()

        print("✅ Retina model loaded")


def load_skin_model():
    global skin_interpreter, skin_input_details, skin_output_details

    if skin_interpreter is None:
        print("Loading Skin model...")
        skin_interpreter = tflite.Interpreter(model_path="./dermnet_quant.tflite")
        skin_interpreter.allocate_tensors()

        skin_input_details = skin_interpreter.get_input_details()
        skin_output_details = skin_interpreter.get_output_details()

        print("✅ Skin model loaded")


def load_chest14_model():
    global chest14_interpreter, chest14_input_details, chest14_output_details

    if chest14_interpreter is None:
        print("Loading Chest14 model...")
        chest14_interpreter = tflite.Interpreter(model_path="./chest_14.tflite")
        chest14_interpreter.allocate_tensors()

        chest14_input_details = chest14_interpreter.get_input_details()
        chest14_output_details = chest14_interpreter.get_output_details()

        print("✅ Chest14 model loaded")


def load_scaler():
    global scaler
    if scaler is None:
        scaler = joblib.load("meta_scaler.pkl")
        print("✅ Scaler loaded")

# ===================================================
# PREPROCESSING
# ===================================================

def preprocess_image(image_bytes, size=(224, 224), gray=False):
    img = Image.open(io.BytesIO(image_bytes))

    if gray:
        img = img.convert("L")
    else:
        img = img.convert("RGB")

    img = img.resize(size)
    img_array = np.array(img) / 255.0

    if gray:
        img_array = np.expand_dims(img_array, axis=-1)

    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype(np.float32)


def preprocess_metadata(age, gender):
    load_scaler()

    age = float(age)
    gender_val = 1 if gender.lower() == "m" else 0

    meta = np.array([[age, gender_val]])
    meta = scaler.transform(meta)

    return meta.astype(np.float32)

# ===================================================
# TB API
# ===================================================

@app.post("/predict/tb")
async def predict_tb(file: UploadFile = File(...), age: float = Form(...), gender: str = Form(...)):
    try:
        load_tb_model()

        contents = await file.read()
        img = preprocess_image(contents, (128, 128), gray=True)
        meta = preprocess_metadata(age, gender)

        tb_interpreter.set_tensor(tb_input_details[0]['index'], img)
        tb_interpreter.set_tensor(tb_input_details[1]['index'], meta)

        tb_interpreter.invoke()

        output = tb_interpreter.get_tensor(tb_output_details[0]['index'])

        prob = float(output[0][0])
        label = "Tuberculosis Detected" if prob > 0.5 else "Normal"

        return {"class": label, "confidence": prob}

    except Exception as e:
        print("❌ TB ERROR:", e)
        return {"error": str(e)}

# ===================================================
# KIDNEY API
# ===================================================

@app.post("/predict/kidney")
async def predict_kidney(file: UploadFile = File(...)):
    try:
        load_kidney_model()

        contents = await file.read()
        img = preprocess_image(contents)

        kidney_interpreter.set_tensor(kidney_input_details[0]['index'], img)
        kidney_interpreter.invoke()

        output = kidney_interpreter.get_tensor(kidney_output_details[0]['index'])

        classes = ["Cyst", "Normal", "Stone", "Tumor"]

        pred = int(np.argmax(output))
        conf = float(np.max(output))

        return {"class": classes[pred], "confidence": conf}

    except Exception as e:
        print("❌ Kidney ERROR:", e)
        return {"error": str(e)}

# ===================================================
# RETINA API
# ===================================================

@app.post("/predict/retina")
async def predict_retina(file: UploadFile = File(...)):
    try:
        load_retina_model()

        contents = await file.read()
        img = preprocess_image(contents)

        retina_interpreter.set_tensor(retina_input_details[0]['index'], img)
        retina_interpreter.invoke()

        output = retina_interpreter.get_tensor(retina_output_details[0]['index'])

        classes = ["ACRIMA", "Glaucoma", "ODIR-5K", "ORIGA", "Cataract", "Retina Disease"]

        pred = int(np.argmax(output))
        conf = float(np.max(output))

        return {"class": classes[pred], "confidence": conf}

    except Exception as e:
        print("❌ Retina ERROR:", e)
        return {"error": str(e)}

# ===================================================
# SKIN API
# ===================================================

@app.post("/predict/skin/dermnet")
async def predict_skin(file: UploadFile = File(...)):
    try:
        load_skin_model()

        contents = await file.read()
        img = preprocess_image(contents)

        skin_interpreter.set_tensor(skin_input_details[0]['index'], img)
        skin_interpreter.invoke()

        output = skin_interpreter.get_tensor(skin_output_details[0]['index'])

        classes = [
            "Acne", "Actinic Keratosis", "Atopic Dermatitis", "Bullous Disease",
            "Cellulitis", "Eczema", "Drug Eruptions", "Hair Loss",
            "Herpes HPV", "Pigmentation Disorders", "Lupus",
            "Melanoma", "Nail Disease", "Contact Dermatitis",
            "Psoriasis", "Scabies", "Benign Tumors",
            "Systemic Disease", "Fungal Infection", "Urticaria",
            "Vascular Tumors", "Vasculitis", "Warts"
        ]

        pred = int(np.argmax(output))
        conf = float(np.max(output))

        return {"class": classes[pred], "confidence": conf}

    except Exception as e:
        print("❌ Skin ERROR:", e)
        return {"error": str(e)}

# ===================================================
# CHEST14 API (NEW)
# ===================================================

@app.post("/predict/chest14")
async def predict_chest14(file: UploadFile = File(...)):
    try:
        load_chest14_model()

        contents = await file.read()
        img = preprocess_image(contents, (224, 224))

        chest14_interpreter.set_tensor(chest14_input_details[0]['index'], img)
        chest14_interpreter.invoke()

        output = chest14_interpreter.get_tensor(chest14_output_details[0]['index'])

        label_columns = [
            'Atelectasis','Cardiomegaly','Consolidation','Edema','Effusion',
            'Emphysema','Fibrosis','Hernia','Infiltration','Mass',
            'Nodule','Pleural_Thickening','Pneumonia','Pneumothorax'
        ]

        probs = output[0]

        threshold = 0.4
        results = []

        for i, prob in enumerate(probs):
            if prob > threshold:
                results.append({
                    "disease": label_columns[i],
                    "confidence": float(prob)
                })

        return {
            "predictions": results,
            "raw": probs.tolist()
        }

    except Exception as e:
        print("❌ Chest14 ERROR:", e)
        return {"error": str(e)}