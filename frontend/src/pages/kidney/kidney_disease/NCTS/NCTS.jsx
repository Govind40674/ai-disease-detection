import React, { useState } from "react";
import axios from "axios";
import styles from "./ncts.module.css";
import Footer from "../../../../components/footer/Footer";
import Header from "../../../../components/header/Header";

function NCTS() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);   // image preview
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {

    const selectedFile = e.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));  // create preview
      setResult(null); // reset old result
    }

  };

  const handleSubmit = async () => {

    if (!file) {
      alert("Please upload a CT scan image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setLoading(true);

      // const response = await fetch(
      //   "http://127.0.0.1:8000/predict/kidney",
      //   {
      //     method: "POST",
      //     body: formData
      //   }
      // );
      const response=await axios.post(`${import.meta.env.VITE_API_URL}/predict/kidney`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      const data = await response.json();

      setResult(data);
      setLoading(false);

    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <>
      <Header/>

      <div className={styles.container}>

        <h1 className={styles.title}>
          Kidney Disease Detection
        </h1>

        <p className={styles.subtitle}>
          Upload Kidney CT Scan Image
        </p>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className={styles.fileInput}
        />

        {/* Image Preview */}
        {preview && (
          <div className={styles.imagePreviewBox}>
            <img
              src={preview}
              alt="Uploaded CT Scan"
              className={styles.previewImage}
            />
          </div>
        )}

        <button
          onClick={handleSubmit}
          className={styles.button}
        >
          Predict
        </button>

        {loading && <p>Analyzing image...</p>}

        {result && (
          <div className={styles.resultBox}>
            <h2>Result</h2>

            <p>
              Disease: <strong>{result.class}</strong>
            </p>

            <p>
              Confidence:{" "}
              <strong>
                {(result.confidence * 100).toFixed(2)}%
              </strong>
            </p>
          </div>
        )}

      </div>

      <Footer/>
    </>
  );
}

export default NCTS;