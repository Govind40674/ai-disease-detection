import React, { useState } from "react";
import axios from "axios";
import styles from "./dermnet.module.css";
import Header from "../../../../components/header/Header";
import Footer from "../../../../components/footer/Footer";

function Dermnet() {

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {

    const file = e.target.files[0];

    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handlePredict = async () => {

    if (!image) {
      alert("Please upload an image first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", image);

    try {

      // const response = await fetch(
      //   "http://localhost:8000/predict/skin/dermnet",
      //   {
      //     method: "POST",
      //     body: formData,
      //   }
      // );
      const response=await axios.post(`${import.meta.env.VITE_API_URL}/predict/skin/dermnet`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })


      const data = await response.data;

      setResult(data.class);
      setConfidence((data.confidence * 100).toFixed(2));

    } catch (error) {
      console.error("Error:", error);
      alert("Prediction failed");
    }

    setLoading(false);
  };

  return (
    <>
    <Header/>

    <div className={styles.container}>

      <h1 className={styles.title}>
        Skin Disease Detection (DermNet AI)
      </h1>

      <div className={styles.uploadBox}>

        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />

        {preview && (
          <img
            src={preview}
            alt="preview"
            className={styles.preview}
          />
        )}

        <button
          onClick={handlePredict}
          className={styles.button}
        >
          Predict Disease
        </button>

      </div>

      {loading && (
        <p className={styles.loading}>
          AI Model is analyzing image...
        </p>
      )}

      {result && (
        <div className={styles.resultBox}>

          <h2>Prediction Result</h2>

          <p>
            <strong>Disease:</strong> {result}
          </p>

          <p>
            <strong>Confidence:</strong> {confidence}%
          </p>

        </div>
      )}

    </div>
    <Footer/>
    </>
  );
}

export default Dermnet;