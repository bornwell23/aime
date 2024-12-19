<template>
  <div class="login-container">
    <div class="login-wrapper">
      <form @submit.prevent="handleLogin" class="login-form">
        <h2>Welcome to Aime</h2>
        
        <p class="login-subtitle">
          {{ firstTimeUser 
            ? 'It looks like you need to create an account first.' 
            : 'Please log in to continue' 
          }}
        </p>
        
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            placeholder="Enter your username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            id="password" 
            v-model="password" 
            required 
            placeholder="Enter your password"
          />
          <button 
            type="button" 
            @click="togglePasswordVisibility" 
            class="password-toggle"
          >
            {{ showPassword ? 'Hide' : 'Show' }}
          </button>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button 
          type="submit" 
          class="login-button" 
          :disabled="isLoading"
        >
          {{ isLoading ? 'Logging In...' : 'Log In' }}
        </button>
        
        <div class="register-link">
          <template v-if="firstTimeUser">
            <p>No account yet? Create one now!</p>
            <button 
              type="button" 
              class="register-button" 
              @click="goToRegister"
            >
              Register
            </button>
          </template>
          <template v-else>
            Don't have an account? 
            <router-link to="/register">Register</router-link>
          </template>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/apiConfig';
import { Logger } from '@common/logger.js';

const logger = new Logger('LoginView');

export default {
  name: 'LoginView',
  props: {
    firstTimeUser: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      error: null,
      isLoading: false
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    goToRegister() {
      logger.info('Navigating to register page');
      this.$router.push('/register');
    },
    async handleLogin() {
      // Set loading state
      this.isLoading = true;
      this.error = null;

      try {
        // Attempt login
        const response = await login(this.username, this.password);
        
        // Log successful login
        logger.info(`User ${this.username} logged in successfully`);
        
        // Redirect to dashboard
        this.$router.push('/dashboard');
      } catch (error) {
        // Handle login errors
        if (error.response) {
          // Server responded with an error
          this.error = error.response.data.detail || 'Login failed';
        } else if (error.request) {
          // Request made but no response received
          this.error = 'No response from server. Please try again.';
        } else {
          // Something happened in setting up the request
          this.error = 'An unexpected error occurred';
        }
        
        // Log the error
        logger.error('Login error', error);
      } finally {
        // Reset loading state
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
}

.login-wrapper {
  width: 100%;
  max-width: 400px;
}

.login-form {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
}

.login-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  position: relative;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.password-toggle {
  position: absolute;
  right: 10px;
  top: 35px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #45a049;
}

.login-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-bottom: 15px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
}

.register-link a {
  color: #4CAF50;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.register-button {
  margin-top: 10px;
  width: 100%;
  padding: 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #1976D2;
}
</style>
