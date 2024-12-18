import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { 
  LoginRequest, 
  AuthTokenResponse, 
  User,
  LoginErrorResponse 
} from '../../../common/types';

// Simulated user database (replace with actual database in production)
const USERS = [
  {
    id: '1',
    username: 'testuser',
    email: 'test@example.com',
    password: bcrypt.hashSync('password123', 10)
  }
];

const JWT_SECRET = process.env.JWT_SECRET || 'your_jwt_secret';
const TOKEN_EXPIRATION = 60 * 60; // 1 hour

const authRouter = express.Router();

// Login Route
authRouter.post('/login', async (req, res) => {
  const { email, password }: LoginRequest = req.body;

  try {
    // Find user by email
    const user = USERS.find(u => u.email === email);

    if (!user) {
      const errorResponse: LoginErrorResponse = {
        code: 'INVALID_CREDENTIALS',
        message: 'Invalid email or password'
      };
      return res.status(401).json(errorResponse);
    }

    // Verify password
    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      const errorResponse: LoginErrorResponse = {
        code: 'INVALID_CREDENTIALS',
        message: 'Invalid email or password'
      };
      return res.status(401).json(errorResponse);
    }

    // Generate tokens
    const accessToken = jwt.sign(
      { userId: user.id, email: user.email }, 
      JWT_SECRET, 
      { expiresIn: TOKEN_EXPIRATION }
    );

    const refreshToken = jwt.sign(
      { userId: user.id, email: user.email }, 
      JWT_SECRET, 
      { expiresIn: '7d' }
    );

    // Prepare response
    const authResponse: AuthTokenResponse = {
      accessToken,
      refreshToken,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        createdAt: new Date().toISOString()
      },
      expiresAt: Math.floor(Date.now() / 1000) + TOKEN_EXPIRATION
    };

    res.json(authResponse);
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      code: 'INTERNAL_SERVER_ERROR', 
      message: 'An unexpected error occurred' 
    });
  }
});

// Logout Route (optional)
authRouter.post('/logout', (req, res) => {
  // In a real app, you might want to invalidate tokens
  res.status(200).json({ message: 'Logged out successfully' });
});

// Token Refresh Route
authRouter.post('/refresh', (req, res) => {
  const { refreshToken } = req.body;

  try {
    // Verify refresh token
    const decoded = jwt.verify(refreshToken, JWT_SECRET) as { 
      userId: string, 
      email: string 
    };

    // Find user
    const user = USERS.find(u => u.id === decoded.userId);

    if (!user) {
      return res.status(401).json({ 
        code: 'UNAUTHORIZED',
        message: 'Invalid refresh token' 
      });
    }

    // Generate new access token
    const newAccessToken = jwt.sign(
      { userId: user.id, email: user.email }, 
      JWT_SECRET, 
      { expiresIn: TOKEN_EXPIRATION }
    );

    const authResponse: AuthTokenResponse = {
      accessToken: newAccessToken,
      refreshToken, // Can reuse existing refresh token or generate new one
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        createdAt: new Date().toISOString()
      },
      expiresAt: Math.floor(Date.now() / 1000) + TOKEN_EXPIRATION
    };

    res.json(authResponse);
  } catch (error) {
    res.status(401).json({ 
      code: 'UNAUTHORIZED',
      message: 'Invalid refresh token' 
    });
  }
});

export default authRouter;
