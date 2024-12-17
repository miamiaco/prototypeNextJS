import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Function to update the user state by fetching from the API
  const fetchUser = async () => {
    try {
      const res = await fetch('api/users/user')
      if (res.status === 200) {
        const data = await res.json();
        setUser(data.user)
      } else {
        throw new Error('Failed to fetch user.');
      }
    } catch (error) {
      console.error(error);
      setUser(null);
    }
  };


  // Function to clear the user state, e.g., during logout
  const clearUser = () => {
    setUser(null);
  };

  useEffect(() => {
      fetchUser()
  }, []);

  useEffect(() => {
      fetchUser();
  }, [])

  return (
    <UserContext.Provider value={{ user, fetchUser, clearUser }}>
      {children}
    </UserContext.Provider>
  );
};
