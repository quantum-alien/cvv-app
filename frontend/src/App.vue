<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="shell">
    <header class="topbar">
      <RouterLink to="/" class="brand">CV&nbsp;Builder</RouterLink>
    </header>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--line);
  background: var(--paper-raised);
}

.brand {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--ink);
  text-decoration: none;
}

.content {
  flex: 1;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}
</style>
