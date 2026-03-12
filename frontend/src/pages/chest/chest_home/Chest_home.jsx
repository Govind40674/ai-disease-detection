import React from 'react'

import Header from "../../../components/header/Header";
import { Link } from 'react-router-dom'
import styles from './chest_home.module.css'
// import Footer from '../../../components/footer/Footer'
import Footer from '../../../components/footer/Footer'

function Chest_home() {
  return (
    <>
    <Header/>
    <div className={styles.container}>
      <h1 className={styles.heading}>Welcome to the Chest Disease Detection System</h1>
      <div className={styles.disease}>
        <div className={styles.disease_card}>
          <img  className={styles.img} src="/chest_X_ray.png" alt="chest-xray" />
          <h2 className={styles.disease_name}>Tuberculosis or Normal</h2>
           <Link to="/chest/tuberculosis" className={styles.link}>Go to Tuberculosis Detection</Link>
            
          </div>
          <div className={styles.disease_card}>
            <img  className={styles.img} src="/chest_X_ray.png" alt="chest-xray" />
          <h2 className={styles.disease_name}>14 disease from</h2>
           <Link to="/chest/14_disease" className={styles.link}>Go to 14 Disease Detection</Link>
          </div>
      </div>

      </div>

      <Footer/>

      

      

    </>
  )
}

export default Chest_home