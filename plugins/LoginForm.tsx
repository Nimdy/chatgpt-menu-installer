import { Formik, Field, Form } from 'formik';
import toast from 'react-hot-toast';
import { useState, useEffect } from 'react';
import axios from 'axios';

type Props = {
  onLoginSuccess: (jwtToken: string) => void;
};

export default function LoginForm({ onLoginSuccess }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios
        .post(
          '/api/validate',
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => onLoginSuccess(token))
        .catch(() => {
          localStorage.removeItem('token');
        });
    }
  }, [onLoginSuccess]);

  const handleSubmit = async (values: { username: string; password: string }) => {
    setIsLoading(true);
    try {
      const response = await axios.post('/api/authenticate', values);
      const { token } = response.data;
      localStorage.setItem('token', token);
      onLoginSuccess(token);
    } catch (error) {
      toast.error('Invalid username or password.');
    }
    setIsLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <Formik
        initialValues={{
          username: '',
          password: '',
        }}
        onSubmit={handleSubmit}
      >
        <Form className="bg-white p-8 rounded-md shadow-md">
          <h1 className="text-2xl font-medium text-gray-800 mb-4">Login</h1>
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 font-medium mb-2">
              Username
            </label>
            <Field
              id="username"
              name="username"
              placeholder="Username"
              className="border border-gray-300 p-2 rounded-md w-full"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-700 font-medium mb-2">
              Password
            </label>
            <Field
              type="password"
              id="password"
              name="password"
              placeholder="Password"
              className="border border-gray-300 p-2 rounded-md w-full"
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </Form>
      </Formik>
    </div>
  );
}
