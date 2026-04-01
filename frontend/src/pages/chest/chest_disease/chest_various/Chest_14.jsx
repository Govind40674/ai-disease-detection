import React, { useState } from 'react'
import styles from './chest_14.module.css'
import Header from '../../../../components/header/Header'
import Footer from '../../../../components/footer/Footer'
import axios from 'axios'


function Chest_14() {

  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  // Handle file select
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)

    if (selectedFile) {
      const imageURL = URL.createObjectURL(selectedFile)
      setPreview(imageURL)
    }
  }

  // Submit to backend
  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload an image")
      return
    }

    setLoading(true)
    setResult(null)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/predict/chest14`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )
        
      

      const data = await res.json()
      setResult(data)
    } catch (error) {
      console.error("Error:", error)
      alert("Error connecting to server")
    }

    setLoading(false)
  }

  return (
    <>
    <Header/>
    <div className={styles.container}>

      <h2>Chest X-ray Disease Detection (Chest14)</h2>

      {/* Upload */}
      <input type="file" accept="image/*" onChange={handleFileChange} />

      {/* Preview */}
      {preview && (
        <div className={styles.previewBox}>
          <h3>Preview:</h3>
          <img src={preview} alt="preview" className={styles.image} />
        </div>
      )}

      {/* Button */}
      <button onClick={handleSubmit} className={styles.button}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {/* Result */}
      {result && (
        <div className={styles.resultBox}>
  <h3>Predictions:</h3>

  <div className={styles.resultGrid}>
    {result.predictions.length === 0 ? (
      <p>No disease detected</p>
    ) : (
      result.predictions.map((item, index) => (
        <div key={index} className={styles.card}>
          <p><strong>{item.disease}</strong></p>
          <p>Confidence: {(item.confidence * 100).toFixed(2)}%</p>
        </div>
      ))
    )}
  </div>
</div>

      )}

    </div>
    <Footer/>
    </>
   
  )
}

export default Chest_14