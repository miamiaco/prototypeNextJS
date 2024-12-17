import React, { useState } from 'react';
import Link from 'next/link';
import Router from 'next/router';
import styles from '../styles/signup.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

const SignupComponent = () => {
    const [showPassword, setShowPassword] = useState(false)
    const [user, setUser] = useState({
          username: '',
          name: '',
          password: '',
      });

      // Handles changes in input fields and updates the user state
      const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({
          ...user,
          [name]: value,
        });
      };

      // Toggles the visibility of the password in the input field
      const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

      // Handles the form submission for user registration
      const handleSubmit = async (e) => {
        e.preventDefault();
        if (!user.username || !user.name || !user.password) {
          alert('Please fill in all fields.');
          return;
        }
        if (user.password.length < 5) {
          alert('Password must be at least 5 characters.');
          return;
        }

        try {
          // Makes a POST request to the registration API endpoint
          const response = await fetch('/api/users/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
          });
          if (!response.ok) {
            throw new Error('Käyttäjänimi on jo käytössä. Valitse toinen.');
          }
          const data = await response.json();
          console.log(data);
          Router.push('/login');
        } catch (error) {
          console.error('Registration Error:', error);
          alert(error.message);
        }
      };

      return (
        <div className={styles.container}>
          <h1 className={styles.title}>miamia</h1>
          <div className={styles.formContainer}>
            <h2 className={styles.secondtitle}> Welcome to your culinary journey</h2>
            <h3 className={styles.thirdtitle}>Rekisteröidy käyttäjäksi</h3>
            <form className={styles.form} onSubmit={handleSubmit}>
              <div>
                <label className={styles.label} htmlFor="username">Käyttäjänimi</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={user.username}
                  onChange={handleChange}
                  className= {styles.inputfield}
                  required
                />
              </div>
              <div>
                <label className={styles.label} htmlFor="name">Nimi</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={user.name}
                  onChange={handleChange}
                  className= {styles.inputfield}
                  required
                />
              </div>
              <div>
                <label className={styles.label} htmlFor="password">Salasana</label>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  value={user.password}
                  onChange={handleChange}
                  className= {styles.inputfield}
                  required
                />
               <button
                  type="button"
                  onClick={togglePasswordVisibility}
                  className={styles.togglePasswordButton}
                  aria-label="Toggle password visibility"
                >
                <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
                </button>
              </div>
              <button className={styles.submitButton} type="submit">Luo profiili</button>
            </form>
            <div className={styles.toOtherPage}>
              Minulla on jo profiili.
                <Link href="/login" className={styles.linkToOtherPage}>
                  Kirjaudu sisään.
                </Link>
              </div>
          </div>
        </div>
      );
};

export default SignupComponent;
