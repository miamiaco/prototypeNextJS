import Link from 'next/link';
import styles from '../styles/navbar.module.css'
import { useRouter } from 'next/router';
import React, { useState } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const router = useRouter();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className={styles.nav}>
      <div className={styles.hamburger} onClick={toggleMenu}>
      <span className={styles.hamburgerLine}></span>
        <span className={styles.hamburgerLine}></span>
        <span className={styles.hamburgerLine}></span>
      </div>
      <ul className={styles.ulList}>
        <li className={styles.liItem}>
          <Link href="/" className={`${styles.link} ${router.pathname === "/" ? styles.active : ""}`}>
            Inspiraatio
          </Link>
        </li>
        <li className={styles.liItem}>
          <Link href="/search" className={`${styles.link} ${router.pathname === "/search" ? styles.active : ""}`}>
            Haku
          </Link>
        </li>
        <li className={styles.liItem}>
          <Link href="/profile" className={`${styles.link} ${router.pathname === "/profile" ? styles.active : ""}`}>
            Tallennetut
          </Link>
        </li>
      </ul>
    </nav>
  );
};


export default Navbar;
