<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useResumeStore } from "@/store/resume";

const store = useResumeStore();
const router = useRouter();

onMounted(() => store.fetchList());

function createNew() {
  store.startNew();
  router.push({ name: "new" });
}

async function remove(id: number) {
  if (!confirm("Delete this CV permanently?")) return;
  await store.remove(id);
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}
</script>

<template>
  <section>
    <div class="head-row">
      <h1>My CVs</h1>
      <button class="btn btn-primary" @click="createNew">+ New CV</button>
    </div>

    <p v-if="store.isLoading">Loading…</p>
    <p v-else-if="store.error" class="error">{{ store.error }}</p>

    <p v-else-if="store.list.length === 0" class="empty">
      You don't have any CVs yet. Click "New CV" to create your first one.
    </p>

    <ul v-else class="list">
      <li v-for="r in store.list" :key="r.id" class="card row">
        <div>
          <h3>{{ r.title }}</h3>
          <p class="muted">
            {{ r.full_name || "No name" }}
            <span v-if="r.job_title"> · {{ r.job_title }}</span>
          </p>
          <p class="muted small">Updated {{ formatDate(r.updated_at) }}</p>
        </div>
        <div class="actions">
          <RouterLink class="btn btn-ghost" :to="{ name: 'preview', params: { id: r.id } }">Preview</RouterLink>
          <RouterLink class="btn btn-ghost" :to="{ name: 'edit', params: { id: r.id } }">Edit</RouterLink>
          <button class="btn btn-danger" @click="remove(r.id)">Delete</button>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.head-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.muted {
  color: var(--muted);
  margin: 0.15rem 0;
}

.small {
  font-size: 0.8rem;
}

.empty {
  color: var(--muted);
  padding: 2rem 0;
}

.error {
  color: var(--danger);
}
</style>
