import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import Feed from '../components/Feed';
import styles from '../styles/feed.module.css';
import Navbar from '@/components/Navbar';
import jwt from 'jsonwebtoken';

export default function App() {
  const [seed, setSeed] = useState('');
  const [batches, setBatches] = useState([]);
  const [showLoadMore, setShowLoadMore] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  // Generate a new seed based on the current timestamp
  const generateNewSeed = () => Date.now().toString();

  // UseEffect hook to load batches of recipes on component mount
  useEffect(() => {
    const loadBatchesSequentially = async () => {
      let currentSeed = Cookies.get('recipeFeedSeed');
      const lastSeedUpdateTime = Cookies.get('lastSeedUpdateTime');
      const currentTime = Date.now();
      const sevenMinutes = 7 * 60 * 1000;

      // Update seed if it's stale or missing
      if (!currentSeed || !lastSeedUpdateTime || currentTime - parseInt(lastSeedUpdateTime, 7) > sevenMinutes) {
        currentSeed = generateNewSeed();
        Cookies.set('recipeFeedSeed', currentSeed, { expires: 1 });
        Cookies.set('lastSeedUpdateTime', currentTime.toString(), { expires: 1 });
      }

      setSeed(currentSeed);

      // Fetch recipes in batches based on feed index
      const feedIndex = Number(sessionStorage.getItem('feedIndex')) || 1;
      for (let i = 1; i <= feedIndex; i++) {
        await fetchRecipes(i, currentSeed);
      }

      setIsLoading(false);
    };

    loadBatchesSequentially();
  }, []);

   // Function to fetch recipes from the server
  const fetchRecipes = async (page, seed) => {
    const response = await fetch(`/api/recipes?page=${page}&seed=${seed}`);
    const newRecipes = await response.json();
    setBatches(prevBatches => [...prevBatches, newRecipes]);
  };

  // Function to load more recipes
  const loadMore = async () => {
    setShowLoadMore(false);

    const currentFeedIndex = Number(sessionStorage.getItem('feedIndex')) || 0;
    const newFeedIndex = currentFeedIndex + 1;

    try {
      await fetchRecipes(newFeedIndex, seed);
      sessionStorage.setItem('feedIndex', newFeedIndex.toString());
    } catch (error) {
      console.error("Failed to fetch more recipes:", error);
    } finally {
      setShowLoadMore(true);
    }
  };

  // UseEffect to restore scroll position after data loads
  useEffect(() => {
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (!isLoading && batches.length && scrollPosition) {
      setTimeout(() => {
        window.scrollTo({
          top: scrollPosition,
          left: 0,
          behavior: "smooth",
        });
      }, 200);
      sessionStorage.removeItem('scrollPosition');
    }
  }, [isLoading, batches]);
  return (
    <div>
      <header>
        <h1>miamia</h1>
      </header>
      <Navbar />
      <Feed batches={batches} />
      {showLoadMore && (
      <button className={styles.loadMoreButton} onClick={loadMore}>Näytä lisää</button>
      )}
      <footer>
      </footer>
    </div>
  );
}


// Function to handle server-side rendering and authentication checks
export async function getServerSideProps(context) {

  const token = context.req.cookies.token;
  const jwtSecret = process.env.JWT_SECRET
  try {
    if (!token) {
      return {
        redirect: {
          destination: '/login',
          permanent: false,
        },
      };
    }
    jwt.verify(token, jwtSecret);
    return { props: {} };
  } catch (error) {

    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
}