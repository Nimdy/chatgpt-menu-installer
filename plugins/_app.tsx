// replace pages/_app.tsx with new code

import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import LoginForm from '../components/Settings/LoginForm';
import { useState, useEffect } from 'react';

import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });
const isBrowser = typeof window !== 'undefined';

function App({ Component, pageProps }: AppProps<{}>) {
  const queryClient = new QueryClient();

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    if (isBrowser) {
      setIsLoggedIn(localStorage.getItem('isLoggedIn') === 'true');
    }
  }, []);

  if (!isLoggedIn) {
    // If the user is not logged in, show the login form
    return (
      <LoginForm
      onLogin={() => setIsLoggedIn(true)}
      username={process.env.NEXT_PUBLIC_USERNAME}
      password={process.env.NEXT_PUBLIC_PASSWORD}
      bypassAuth={process.env.NEXT_PUBLIC_BYPASS_LOGIN === 'true'}
    />
    );
  }

  return (
    <div className={inter.className}>
      <Toaster />
      <QueryClientProvider client={queryClient}>
        <Component {...pageProps} />
      </QueryClientProvider>
    </div>
  );
}

export default appWithTranslation(App);
