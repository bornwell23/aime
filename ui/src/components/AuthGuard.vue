<template>
  <div>
    <LoginModal 
      v-if="!isAuthenticated" 
      @login="login" 
      @close="logout"
    />
    <slot v-if="isAuthenticated"></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getCurrentUser, login, logout } from '@/services/apiConfig';
import { Logger } from '@common/logger.js';
import LoginModal from './LoginModal.vue';

const logger = new Logger('AuthGuard');

export default defineComponent({
  name: 'AuthGuard',
  setup() {
    const isAuthenticated = ref(false);
    const currentUser = ref(null);

    const checkAuthentication = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        isAuthenticated.value = false;
        currentUser.value = null;
        return;
      }

      try {
        const response = await getCurrentUser();
        currentUser.value = response.data;
        isAuthenticated.value = true;
        logger.info('User authenticated successfully');
      } catch (error) {
        // Clear token if getCurrentUser fails
        localStorage.removeItem('authToken');
        isAuthenticated.value = false;
        currentUser.value = null;
        logger.warn('Authentication check failed', error);
      }
    };

    onMounted(checkAuthentication);

    return {
      isAuthenticated,
      currentUser,
      login: async (username: string, password: string) => {
        try {
          await login(username, password);
          await checkAuthentication();
        } catch (error) {
          logger.error('Login failed', error);
          throw error;
        }
      },
      logout: () => {
        localStorage.removeItem('authToken');
        isAuthenticated.value = false;
        currentUser.value = null;
        logout();
      }
    };
  },
  components: {
    LoginModal
  }
});
</script>
