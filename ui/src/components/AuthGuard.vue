<template>
  <div>
    <router-view v-slot="{ Component }">
      <template v-if="!isAuthenticated && Component !== Register">
        <Login 
          v-if="Component === Login"
          :firstTimeUser="!hasEverLoggedIn"
        />
        <component 
          v-else 
          :is="Component"
        />
      </template>
      <component 
        v-else 
        :is="Component"
      />
    </router-view>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getCurrentUser } from '@/services/apiConfig';
import { Logger } from '/app/common/logger.js';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';

const logger = new Logger('AuthGuard');

export default defineComponent({
  name: 'AuthGuard',
  components: {
    Login,
    Register
  },
  setup() {
    const isAuthenticated = ref(false);
    const currentUser = ref(null);
    const hasEverLoggedIn = ref(false);

    const checkAuthentication = async () => {
      const token = localStorage.getItem('authToken');
      const previousLoginAttempts = localStorage.getItem('loginAttempts');
      
      // Check if there have been any previous login attempts
      hasEverLoggedIn.value = !!previousLoginAttempts;

      if (!token) {
        isAuthenticated.value = false;
        currentUser.value = null;
        return;
      }

      try {
        const response = await getCurrentUser();
        currentUser.value = response.data;
        isAuthenticated.value = true;
        
        // Mark that a successful login has occurred
        localStorage.setItem('loginAttempts', 'true');
        
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
      hasEverLoggedIn
    };
  }
});
</script>
