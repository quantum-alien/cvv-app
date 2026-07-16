<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useResumeStore } from "@/store/resume";

const route = useRoute();
const store = useResumeStore();
const resumeId = Number(route.params.id);

onMounted(() => store.fetchOne(resumeId));

const resume = computed(() => store.current);

function formatDate(iso: string | null) {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString("en-US", { month: "short", year: "numeric" });
}

function period(start: string | null, end: string | null, isCurrent = false) {
  const from = formatDate(start);
  const to = isCurrent ? "present" : formatDate(end);
  return [from, to].filter(Boolean).join(" — ");
}

function print() {
  window.print();
}
</script>

<template>
  <section>
    <div class="toolbar no-print">
      <RouterLink class="btn btn-ghost" :to="{ name: 'edit', params: { id: resumeId } }">← Edit</RouterLink>
      <button class="btn btn-primary" @click="print">Print / Save as PDF</button>
    </div>

    <article class="paper">
      <header class="paper-header">
        <h1>{{ resume.full_name || "No name" }}</h1>
        <p v-if="resume.job_title" class="job-title">{{ resume.job_title }}</p>
        <p class="contacts">
          <span v-if="resume.email">{{ resume.email }}</span>
          <span v-if="resume.phone"> · {{ resume.phone }}</span>
          <span v-if="resume.address"> · {{ resume.address }}</span>
        </p>
      </header>

      <section v-if="resume.summary" class="paper-section">
        <h2>Summary</h2>
        <p>{{ resume.summary }}</p>
      </section>

      <section v-if="resume.experiences.length" class="paper-section">
        <h2>Work experience</h2>
        <div v-for="(exp, i) in resume.experiences" :key="i" class="entry">
          <div class="entry-head">
            <strong>{{ exp.position }}</strong>
            <span class="period">{{ period(exp.start_date, exp.end_date, exp.is_current) }}</span>
          </div>
          <div class="entry-sub">{{ exp.company }}</div>
          <p v-if="exp.description">{{ exp.description }}</p>
        </div>
      </section>

      <section v-if="resume.educations.length" class="paper-section">
        <h2>Education</h2>
        <div v-for="(edu, i) in resume.educations" :key="i" class="entry">
          <div class="entry-head">
            <strong>{{ edu.institution }}</strong>
            <span class="period">{{ period(edu.start_date, edu.end_date) }}</span>
          </div>
          <div class="entry-sub">
            {{ edu.degree }}<span v-if="edu.field_of_study"> · {{ edu.field_of_study }}</span>
          </div>
        </div>
      </section>

      <section v-if="resume.skills.length" class="paper-section">
        <h2>Skills</h2>
        <ul class="skills">
          <li v-for="(s, i) in resume.skills" :key="i">
            {{ s.name }}
            <span class="dots">
              <span v-for="n in 5" :key="n" class="dot" :class="{ filled: n <= s.level }"></span>
            </span>
          </li>
        </ul>
      </section>
    </article>
  </section>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.paper {
  background: var(--paper-raised);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 3rem;
  max-width: 720px;
  margin: 0 auto;
}

.paper-header h1 {
  font-size: 2rem;
}

.job-title {
  color: var(--accent);
  font-weight: 600;
  margin: 0.2rem 0;
}

.contacts {
  color: var(--muted);
  font-size: 0.9rem;
}

.paper-section {
  margin-top: 1.75rem;
}

.paper-section h2 {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.3rem;
  margin-bottom: 0.8rem;
}

.entry {
  margin-bottom: 1rem;
}

.entry-head {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.entry-sub {
  color: var(--muted);
  font-size: 0.9rem;
}

.period {
  color: var(--muted);
  font-size: 0.85rem;
  white-space: nowrap;
}

.skills {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
}

.dots {
  display: inline-flex;
  gap: 0.2rem;
  margin-left: 0.5rem;
  vertical-align: middle;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--line);
  display: inline-block;
}

.dot.filled {
  background: var(--accent);
}

@media print {
  .no-print {
    display: none !important;
  }
  .paper {
    border: none;
    padding: 0;
  }
}
</style>
