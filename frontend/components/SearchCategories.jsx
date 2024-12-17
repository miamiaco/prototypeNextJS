import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import styles from '../styles/searchcategories.module.css';
import SaveRecipeModal from './SaveButton';

function shuffle(array) {
  let currentIndex = array.length, randomIndex;
  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }
  return array;
}

// Helper function to shuffle categories and their respective recipes
function getShuffledCategories(categories) {
  return categories.map(category => {
    const shuffledRecipes = shuffle([...category.recipes]);
    return {
      ...category,
      recipes: shuffledRecipes,
      coverImage: shuffledRecipes[0] ? shuffledRecipes[0].firstImage : null
    };
  });
}


function CategoriesComponent({ categories }) {
  const [shuffledCategories, setShuffledCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [currentRecipe, setCurrentRecipe] = useState(null);
  const [visibleRecipeSets, setVisibleRecipeSets] = useState({});

  useEffect(() => {
      const tenMinutes = 10 * 60 * 1000; // 10 minutes until updates
      const cachedData = localStorage.getItem('shuffledCategoriesCache');
      const now = new Date().getTime();
      let data = cachedData ? JSON.parse(cachedData) : null;

      // Check if cache exists and it hasn't expired
      if (data && (now - data.timestamp) < tenMinutes) {
        setShuffledCategories(data.shuffledCategories);
      } else {
        const newShuffledCategories = getShuffledCategories(categories);
        setShuffledCategories(shuffle(newShuffledCategories));
        localStorage.setItem('shuffledCategoriesCache', JSON.stringify({
          shuffledCategories: newShuffledCategories,
          timestamp: now
        }));
      }
    }, [categories]);

  // Handles category selection to toggle display of recipes
  const handleCategoryClick = (category) => {
    if (selectedCategory === category) {
      setSelectedCategory(null);
    } else {
      setSelectedCategory(category); // Open the clicked category
      // Initialize visible sets for a newly selected category if not already set
      if (!visibleRecipeSets[category]) {
        setVisibleRecipeSets({ ...visibleRecipeSets, [category]: 1 });
      }
    }
  };

  // Function to handle recipe save button click
  const handleSaveClick = (recipe) => {
    setCurrentRecipe(recipe);
    setShowSaveModal(true);
    console.log(recipe)
  };

  // Function to load more recipes for a given category
  const loadMoreRecipes = (category) => {
    // Increment the number of visible recipe sets for the category
    setVisibleRecipeSets({
      ...visibleRecipeSets,
      [category]: (visibleRecipeSets[category] || 1) + 1,
    });
  };

  return (
    <div className={styles.gridContainer}>
      <div className={styles.buttonContainer}>
        {selectedCategory && (
          <button
            id="backButton"
            className={`${styles.backButton} ${selectedCategory ? '' : styles.hidden}`}
            onClick={() => setSelectedCategory(null)}
            aria-label="Back to categories"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="44" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={styles.backIcon}>
              <path d="M19 12H5"></path>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
          </button>
        )}
      </div>
      {shuffledCategories.map((categoryData, index) => {
        // If a category is selected and it's not the current one, don't render it
        if (selectedCategory && selectedCategory !== categoryData.category) {
          return null;
        }

        return (
          <div key={index} className={styles.categoryItem}>
            <div className={styles.catgoryWrapper}>
              <h2
                className={styles.categoryTitle}
                onClick={() => handleCategoryClick(categoryData.category)}
                role="button"
                tabIndex={0}
              >
                {categoryData.category}
              </h2>

              {selectedCategory !== categoryData.category && categoryData.coverImage && (
                <div
                  className={styles.categoryImageWrapper}
                  onClick={() => handleCategoryClick(categoryData.category)}
                  role="button"
                  tabIndex={0}
                >
                  <Image
                    src={categoryData.coverImage}
                    alt={`${categoryData.category} cover`}
                    layout="fill"
                    objectFit="cover"
                    className={styles.categoryImage}
                    blurDataURL={'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='}
                    placeholder='blur'
                    priority
                  />
                </div>
              )}
            </div>

            {selectedCategory === categoryData.category && (
              Array.from({ length: visibleRecipeSets[categoryData.category] || 1 }).map((_, setIndex) => (
                <div key={setIndex} className={styles.recipesGrid}>
                  {categoryData.recipes.slice(setIndex * 20, (setIndex + 1) * 20).map((recipe) => (
                    <div key={recipe.id} className={styles.recipeBlock}>
                      <div className={styles.recipeCard} style={{ position: 'relative' }}>
                        <Link href={`/${recipe.title}`}>
                          <div className={styles.recipeImageWrapper}>
                            <Image
                              width={200}
                              height={500}
                              src={recipe.firstImage}
                              alt={recipe.title}
                              layout="responsive"
                              className={styles.recipeImage}
                              blurDataURL={'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='}
                              placeholder='blur'
                              priority
                            />
                          </div>
                        </Link>
                        <div className={styles.ownerName}>{recipe.owner}</div>
                        <button className={styles.buttonAtFirst} onClick={() => handleSaveClick(recipe)}>+</button>
                      </div>
                      <h2 className={styles.recipeTitle}><Link href={`/${recipe.title}`}>{recipe.title}</Link></h2>
                    </div>
                  ))}
                </div>
              ))
            )}
            {selectedCategory === categoryData.category && categoryData.recipes.length > (visibleRecipeSets[categoryData.category] || 1) * 30 && (
              <div className={styles.loadMoreContainer}>
                <button onClick={() => loadMoreRecipes(categoryData.category)} className={styles.loadMoreButton}>
                  Näytä lisää
                </button>
              </div>
            )}
          </div>
        );
      })}
      {showSaveModal && <SaveRecipeModal recipe={currentRecipe} setShowSaveModal={setShowSaveModal} />}
    </div>
  );
}

export default CategoriesComponent;
