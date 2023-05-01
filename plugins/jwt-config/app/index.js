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
    return res.send(403).json({
      success: false,
      message: 'Incorrect username or password'
    });
  }
});

app.listen(3000, () => {
  console.log('Authentication service started on port 3000');
});
