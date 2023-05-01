const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

app.post('/api/authenticate', (req, res) => {
  const { username, password } = req.body;
  
  // Replace with your own logic to validate username and password
  const mockUsername = "admin";
  const mockPassword = "password";
  
  if (username === mockUsername && password === mockPassword) {
    const token = jwt.sign({username}, process.env.NEXT_PUBLIC_JWT_SECRET, { expiresIn: '1d' });
    return res.json({
      success: true,
      message: 'Authentication successful!',
      token: token
    });
  } else {
    return res.status(403).json({
      success: false,
      message: 'Incorrect username or password'
    });
  }
});

// New route to validate JWT tokens
app.post('/api/validate', (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ success: false, message: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  try {
    jwt.verify(token, process.env.NEXT_PUBLIC_JWT_SECRET);
    return res.json({ success: true, message: 'Token is valid' });
  } catch (error) {
    return res.status(401).json({ success: false, message: 'Invalid token' });
  }
});

app.listen(3000, () => {
  console.log('Authentication service started on port 3000');
});
