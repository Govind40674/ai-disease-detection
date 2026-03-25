import React, { useState } from "react";
import axios from "axios";
import styles from "./retinal_fundus.module.css";
import Footer from "../../../../components/footer/Footer";
import Header from "../../../../components/header/Header";

function Retinal_fundus() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleSubmit = async () => {

    if (!file) {
      alert("Please upload an image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/predict/retina`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("API RESPONSE:", response.data); // 🔥 DEBUG

      // ✅ CHECK RESPONSE SAFELY
      if (!response || !response.data) {
        alert("No response from server");
        setLoading(false);
        return;
      }

      // ✅ HANDLE BACKEND ERROR
      if (response.data.error) {
        alert(response.data.error);
        setLoading(false);
        return;
      }

      // ✅ SAFE DATA ACCESS
      setResult(response.data.class || "Unknown");
      setConfidence(
        response.data.confidence
          ? (response.data.confidence * 100).toFixed(2)
          : "0"
      );

      setLoading(false);

    } catch (error) {
      console.error("AXIOS ERROR:", error);
      setLoading(false);
      alert("Server error or model crashed");
    }
  };

  return (
    <>
      <Header />

      <div className={styles.container}>
        <h1>Retinal Fundus Disease Detection</h1>

        <p>Upload a retinal fundus image to detect eye diseases.</p>
        <p>Otherwise, its prediction is not accurate.</p>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />

        {preview && (
          <div className={styles.previewBox}>
            <img src={preview} alt="preview" className={styles.previewImage} />
          </div>
        )}

        <button className={styles.open} onClick={handleSubmit}>
          Predict Disease
        </button>

        {loading && <p>Analyzing image...</p>}

        {/* ✅ SAFE RENDER */}
        {result && (
          <div className={styles.result}>
            <h2>Prediction: {result}</h2>
            <h3>Confidence: {confidence}%</h3>
          </div>
        )}
      </div>

      <Footer />
    </>
  );
}

export default Retinal_fundus;
