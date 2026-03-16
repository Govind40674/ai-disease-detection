import React, { useEffect } from 'react'
import Header from "../../components/header/Header";
import First_page from '../../components/first_page/First_page'
import Footer from '../../components/footer/Footer';
import styles from './home.module.css'

function Home() {

  useEffect(() => {
    document.body.classList.add("home-body")

    return () => {
      document.body.classList.remove("home-body")
    }
  }, [])

  return (
    <>
      <Header/>
      <First_page/>
      <Footer/>
    </>
  )
}

export default Home