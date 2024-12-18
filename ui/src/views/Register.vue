<template>
  <div class="register-container">
    <form @submit.prevent="handleRegister" class="register-form">
      <h2>Create an Account</h2>
      
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          required 
          minlength="3" 
          maxlength="50"
          placeholder="Choose a username"
        />
      </div>
      
      <div class="form-group">
        <label for="email">Email</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          required 
          placeholder="Enter your email"
        />
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          :type="showPassword ? 'text' : 'password'" 
          id="password" 
          v-model="password" 
          required 
          minlength="8"
          pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
          title="Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"
          placeholder="Create a strong password"
        />
        <button 
          type="button" 
          @click="togglePasswordVisibility" 
          class="password-toggle"
        >
          {{ showPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
      
      <div class="form-group">
        <label for="confirm-password">Confirm Password</label>
        <input 
          :type="showConfirmPassword ? 'text' : 'password'" 
          id="confirm-password" 
          v-model="confirmPassword" 
          required 
          placeholder="Repeat your password"
        />
        <button 
          type="button" 
          @click="toggleConfirmPasswordVisibility" 
          class="password-toggle"
        >
          {{ showConfirmPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <button 
        type="submit" 
        class="register-button" 
        :disabled="isLoading"
      >
        {{ isLoading ? 'Creating Account...' : 'Register' }}
      </button>
      
      <div class="login-link">
        Already have an account? 
        <router-link to="/login">Log in</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { register } from '@/services/apiConfig';
import logger from '../../../common/logger';

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
      error: null,
      isLoading: false
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    validateForm() {
      // Clear previous errors
      this.error = null;

      // Check password match
      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match';
        return false;
      }

      // Validate password complexity
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      if (!passwordRegex.test(this.password)) {
        this.error = 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character';
        return false;
      }

      return true;
    },
    async handleRegister() {
      // Validate form before submission
      if (!this.validateForm()) {
        return;
      }

      // Set loading state
      this.isLoading = true;
      this.error = null;

      try {
        // Attempt registration
        await register(this.username, this.email, this.password);
        
        // Log successful registration
        logger.info(`User ${this.username} registered successfully`);
        
        // Redirect to login or show success message
        this.$router.push('/login');
      } catch (error) {
        // Handle registration errors
        if (error.response) {
          // Server responded with an error
          this.error = error.response.data.detail || 'Registration failed';
        } else if (error.request) {
          // Request made but no response received
          this.error = 'No response from server. Please try again.';
        } else {
          // Something happened in setting up the request
          this.error = 'An unexpected error occurred';
        }
        
        // Log the error
        logger.error('Registration error', error);
      } finally {
        // Reset loading state
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
}

.register-form {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
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

.register-button {
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

.register-button:hover {
  background-color: #45a049;
}

.register-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-bottom: 15px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
}

.login-link a {
  color: #4CAF50;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
