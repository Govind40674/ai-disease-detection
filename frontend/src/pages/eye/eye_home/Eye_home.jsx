import React from 'react'
import styles from './eye_home.module.css'
import Footer from '../../../components/footer/Footer'
import Header from '../../../components/header/Header'
import { Link } from 'react-router-dom'

function Eye_home() {
  return (
    <>
    <Header/>

    <div className={styles.container}>
      <h1 className={styles.heading}>Welcome to the Eye Disease Detection System</h1>
      <div className={styles.disease}>
        <div className={styles.disease_card}>
          <img  className={styles.img} src="/eye.png" alt="chest-xray" />
          <h2 className={styles.disease_name}>Retinal Fundus Image</h2>
          <Link to="/eye/retinal_fundus" className={styles.link}>Go to eye disease detection</Link>
        </div>
      </div>
    </div>
    <Footer/>



    </>

   
   
  )
}

export default Eye_home