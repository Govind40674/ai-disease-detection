import React from 'react'
import styles from './skin_home.module.css'
import Footer from '../../../components/footer/Footer'
import Header from '../../../components/header/Header'
import { Link } from 'react-router-dom'

function Skin_home() {
  return (
    <>
      <Header />
      <div className={styles.container}>
        <h1 className={styles.heading}>Welcome to the Skin Disease Detection System</h1>
        <div className={styles.disease}>
          <div className={styles.disease_card}>
            <img className={styles.img} src="/skin.png" alt="skin-disease" />
            <h2 className={styles.disease_name}>Skin Disease Detection</h2>
            <Link to="/skin/disease_detection" className={styles.link}>Go to skin disease detection</Link>
          </div>
        </div>
      </div>
      <Footer />
    </>

  
  )
}

export default Skin_home