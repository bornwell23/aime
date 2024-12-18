<template>
  <div class="login-modal">
    <div class="modal-content">
      <h2>Login</h2>
      <form @submit.prevent="submitLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            id="username" 
            v-model="username" 
            type="text" 
            required 
            placeholder="Enter your username"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            required 
            placeholder="Enter your password"
          />
        </div>
        <div class="form-actions">
          <button 
            type="submit" 
            :disabled="!isFormValid"
          >
            Login
          </button>
          <button 
            type="button" 
            @click="$emit('close')"
          >
            Cancel
          </button>
        </div>
        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { login } from '@/services/apiConfig';
import { Logger } from '@common/logger.js';

const logger = new Logger('LoginModal');

export default defineComponent({
  name: 'LoginModal',
  emits: ['login', 'close'],
  setup(props, { emit }) {
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');

    const isFormValid = computed(() => 
      username.value.trim().length > 0 && 
      password.value.trim().length > 0
    );

    const submitLogin = async () => {
      try {
        errorMessage.value = '';
        await login(username.value, password.value);
        
        // Emit login success event
        emit('login', { username: username.value });
        
        logger.info('Login successful');
      } catch (error) {
        // Handle login error
        errorMessage.value = error.response?.data?.detail || 'Login failed';
        logger.error('Login failed', error);
      }
    };

    return {
      username,
      password,
      errorMessage,
      isFormValid,
      submitLogin
    };
  }
});
</script>

<style scoped>
.login-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.error-message {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>
