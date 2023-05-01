import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import LoginForm from '../components/Settings/LoginForm';
import { useAuthToken } from '../utils/app/auth';

import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {
  const queryClient = new QueryClient();

  const { token: authToken, setToken: setAuthToken } = useAuthToken();
  const bypassAuth = process.env.NEXT_PUBLIC_BYPASS_LOGIN === 'true';

  if (!authToken && !bypassAuth) {
    // If the user is not logged in and not bypassing auth, show the login form
    return (
      <LoginForm
        onLoginSuccess={(jwtToken) => setAuthToken(jwtToken)}
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
