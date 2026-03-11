import React from 'react'
import styles  from  './Footer.module.css'
import { FaFacebook, FaTwitter, FaInstagram, FaGithub } from 'react-icons/fa';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <>
    <div className={styles.container}>
    <div className={styles.footer}>
      <p>Copyright © 2024. All rights reserved by Team 4</p>
    </div>
    <div className={styles.link}>
      <Link to="/" className={styles.linkItem}>Home</Link>
      <Link to="/about" className={styles.linkItem}>About</Link>
      
    </div>
    <div className={styles.section}>
          <h4>Follow Me</h4>

          <div className={styles.social}>

            <a 
              href="https://facebook.com/Govind Kumar"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaFacebook />
            </a>

            <a 
              href="https://instagram.com/itz_govindkumar"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaInstagram />
            </a>

            <a 
              href="https://github.com/Govind40674"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaGithub />
            </a>

            <a 
              href="https://twitter.com/Govind_Kumar"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaTwitter />
            </a>

          </div>

        </div>
        </div>
    
    </>
  )
}

export default Footer