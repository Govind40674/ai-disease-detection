import React from 'react'
import {Link } from 'react-router-dom'
import Header from '../../../components/header/Header'
import styles from './kidney_home.module.css'
import Footer from '../../../components/footer/Footer'

function Kidney_home() {
  return (
    <>
    <Header/>
      
    <div className={styles.container}>
      <h1 className={styles.heading}>Welcome to the Kidney Disease Detection System</h1>
      <div className={styles.disease}>
        <div className={styles.disease_card}>
          <img  className={styles.img} src="/ct_scan_kidney.png" alt="chest-xray" />
          <h2 className={styles.disease_name}>Kidney Disease</h2>
          <Link to="/kidney/ncts" className={styles.link}>Go to Kidney Disease Detection</Link>
        </div>
      </div>
    </div>
    <Footer/>


    </>
  )
}

export default Kidney_home