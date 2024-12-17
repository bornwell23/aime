<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
    </div>
    <div class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Conversations</h3>
          <div class="stat-value">128</div>
        </div>
        <div class="stat-card">
          <h3>Messages Today</h3>
          <div class="stat-value">24</div>
        </div>
        <div class="stat-card">
          <h3>Average Response Time</h3>
          <div class="stat-value">1.2s</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped>
.dashboard {
  padding: var(--spacing-lg);
  min-height: 100vh;
  background-color: var(--color-background);
}

.dashboard-header {
  margin-bottom: var(--spacing-xl);
}

.dashboard-header h1 {
  color: var(--color-text);
  font-size: 2rem;
  font-weight: 600;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  background-color: var(--color-surface-raised);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: 0 2px 8px var(--color-shadow);
  transition: transform var(--transition-fast);
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card h3 {
  color: var(--color-text-secondary);
  font-size: 1rem;
  margin-bottom: var(--spacing-md);
}

.stat-value {
  color: var(--color-text);
  font-size: 2rem;
  font-weight: 600;
}
</style>
