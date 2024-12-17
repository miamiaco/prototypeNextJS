import React, { useState } from 'react';
import Link from 'next/link';
import Router from 'next/router';
import styles from '../styles/login.module.css';
import { useUser } from '../contexts/UserContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

const LoginComponent = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { fetchUser } = useUser()
    const [showPassword, setShowPassword] = useState(false)

    // Handles form submission for user login
    async function handleSubmit(e) {
      e.preventDefault();
      const loginResponse = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      // Navigate to home if login is successful, otherwise display error
      if (loginResponse.ok) {
        await fetchUser();
        Router.push('/');
      } else {
        const errorData = await loginResponse.json();
        setError(errorData.error);
      }
    }

    // Toggles the visibility of the password field
    const togglePasswordVisibility = () => {
      setShowPassword(!showPassword);
  };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>miamia</h1>
            <div className={styles.formContainer}>
            <h2 className={styles.secondtitle}> Lets bring the magic back to the kitchen</h2>
            <h3 className={styles.thirdtitle}>Kirjaudu sisään</h3>
              <form onSubmit={handleSubmit} className={styles.form}>
              <div>
                  <label htmlFor="username" className={styles.label}>Käyttäjänimi</label>
                  <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className={styles.inputfield}
                  />
              </div>
              <div>
                  <label htmlFor="password" className={styles.label}>Salasana</label>
                  <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={styles.inputfield}
                  />
                  <button
                    type="button"
                    onClick={togglePasswordVisibility}
                    className={styles.togglePasswordButton}
                    aria-label="Toggle password visibility"
                  >
                <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye}/>
                </button>
              </div>
              <button type="submit" className={styles.submitButton}>Kirjaudu sisään</button>
              {error && <p className={styles.errorMessage}>{error}</p>}
              </form>
              <div className={styles.toOtherPage}>
                Minulla ei ole vielä profiilia.
                  <Link href="/signup" className={styles.linkToOtherPage}>
                    Luo profiili.
                  </Link>
              </div>
            </div>
        </div>
      );
};

export default LoginComponent;
