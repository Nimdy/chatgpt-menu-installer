import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import LoginForm from '../components/Settings/LoginForm';
import { useState, useEffect } from 'react';
import { useAuthToken } from '../util/auth';

import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {
  const queryClient = new QueryClient();

  const [authToken, setAuthToken] = useAuthToken();
  const bypassAuth = process.env.NEXT_PUBLIC_BYPASS_LOGIN === 'true';

  useEffect(() => {
    if (bypassAuth) {
      setAuthToken('bypass');
    }
  }, [bypassAuth, setAuthToken]);

  if (!authToken && !bypassAuth) {
    // If the user is not logged in and not bypassing auth, show the login form
    return (
      <LoginForm
        onLogin={setAuthToken}
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
