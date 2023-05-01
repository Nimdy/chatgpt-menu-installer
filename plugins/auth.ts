import { useState, useEffect } from 'react';

export const useAuthToken = () => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Check if the code is running in the browser
    if (typeof window !== 'undefined') {
      // Get the token from localStorage and set it as the initial state
      setToken(localStorage.getItem('token'));
    }
  }, []);

  // Save the token to localStorage and update the state
  const saveToken = (jwtToken: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', jwtToken);
      setToken(jwtToken);
    }
  };

  // Remove the token from localStorage and update the state
  const removeToken = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      setToken(null);
    }
  };

  // Return the token, saveToken function, and removeToken function
  return {
    token,
    setToken: saveToken,
    removeToken,
  };
};
