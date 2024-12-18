<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <AuthGuard>
      <div class="container mx-auto p-6">
        <header class="bg-white shadow-md rounded-lg p-4 mb-6">
          <h1 class="text-2xl font-bold text-gray-800">
            Welcome to the Application
          </h1>
        </header>
        
        <main>
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4">
              Authenticated Content
            </h2>
            <p>You are now logged in and can access protected features.</p>
            
            <button 
              @click="logout" 
              class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
              Logout
            </button>
          </div>
        </main>
      </div>
    </AuthGuard>
  </div>
</template>

<script lang="ts">
import { useAuthStore } from '@stores/authStore';
import AuthGuard from './components/AuthGuard.vue';

export default {
  name: 'App',
  components: {
    AuthGuard
  },
  setup() {
    const authStore = useAuthStore();
    
    const logout = () => {
      authStore.logout();
    };

    return {
      logout
    };
  }
};
</script>

<style>
/* Global styles or imports */
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
</style>
