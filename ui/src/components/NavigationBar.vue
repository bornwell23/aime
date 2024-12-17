<template>
  <nav class="nav-bar">
    <router-link to="/" class="nav-link" active-class="active">
      <i class="fas fa-comment"></i>
      <span>Chat</span>
    </router-link>
    <router-link to="/dashboard" class="nav-link" active-class="active">
      <i class="fas fa-chart-bar"></i>
      <span>Dashboard</span>
    </router-link>
    <router-link to="/history" class="nav-link" active-class="active">
      <i class="fas fa-history"></i>
      <span>History</span>
    </router-link>
  </nav>
</template>

<script>
export default {
  name: 'NavigationBar'
}
</script>

<style scoped>
.nav-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: var(--color-surface-raised);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -2px 10px var(--color-shadow);
  z-index: 100; /* Higher than chat control */
  padding-bottom: env(safe-area-inset-bottom); /* For devices with bottom safe area */
}

.nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
  border-radius: var(--radius-sm);
}

.nav-link i {
  font-size: 1.2rem;
}

.nav-link span {
  font-size: 0.8rem;
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: var(--color-surface);
}

.nav-link.active {
  color: var(--color-primary);
}

.nav-link.active i {
  transform: scale(1.1);
}
</style>
