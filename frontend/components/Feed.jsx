import React, { useState } from 'react';
import Link from 'next/link';
import styles from '../styles/feed.module.css';
import Image from 'next/image';
import SaveRecipeModal from './SaveButton';


export default function Feed({ batches }) {

  const [showSaveModal, setShowSaveModal] = useState(false);
  const [currentRecipe, setCurrentRecipe] = useState(null);

  // Function to handle click event for saving a recipe
  const handleSaveClick = (recipe) => {
    setCurrentRecipe(recipe);
    setShowSaveModal(true);
  };

  return (
    <div>
      {batches.map((recipes, batchIndex) => (
        <div key={batchIndex} className={styles.batchContainer}>
          <div className={styles.feedcontainer}>
            {recipes.map(recipe => (
              <div className={styles.recipeBlock} key={recipe._id}>
                <div className={styles.recipeCard} >
                  <Link href={`/${recipe.title}`}
                  onClick={() =>
                    sessionStorage.setItem('scrollPosition', window.pageYOffset)
                  }>
                    <Image
                      width={200}
                      height={500}
                      style={{ width: '100%', height: '100%' }}
                      className={styles.recipeImage}
                      src={recipe.firstImageUrl}
                      alt={recipe.title}
                      layout="responsive"
                      blurDataURL={'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='}
                      placeholder='blur'
                      priority
                    />
                    </Link>
                  <div className={styles.ownerName}>{recipe.owner}</div>
                  <button className={styles.buttonAtFirst} onClick={() => handleSaveClick(recipe)}>+</button>
                </div>
                <h2 className={styles.recipeTitle}><Link href={`/${recipe.title}`}
                onClick={() =>
                    sessionStorage.setItem('scrollPosition', window.pageYOffset)
                  }
                  >{recipe.title}</Link></h2>
              </div>
            ))}
          </div>
        </div>
      ))}
      {showSaveModal && <SaveRecipeModal recipe={currentRecipe} setShowSaveModal={setShowSaveModal} />}
    </div>
  );
}
