// util/auth.ts
import { useState } from 'react';

export const useAuthToken = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const saveToken = (jwtToken: string) => {
    localStorage.setItem('token', jwtToken);
    setToken(jwtToken);
  };

  const removeToken = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return {
    token,
    setToken: saveToken,
    removeToken,
  };
};
