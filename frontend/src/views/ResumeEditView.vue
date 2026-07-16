<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useResumeStore } from "@/store/resume";
import type { Education, Experience, Skill } from "@/types/resume";

const route = useRoute();
const router = useRouter();
const store = useResumeStore();

const resumeId = route.params.id ? Number(route.params.id) : null;

onMounted(async () => {
  if (resumeId) {
    await store.fetchOne(resumeId);
  } else {
    store.startNew();
  }
});

function addExperience() {
  const item: Experience = {
    company: "",
    position: "",
    start_date: null,
    end_date: null,
    is_current: false,
    description: "",
    order: store.current.experiences.length,
  };
  store.current.experiences.push(item);
}

function addEducation() {
  const item: Education = {
    institution: "",
    degree: "",
    field_of_study: "",
    start_date: null,
    end_date: null,
    order: store.current.educations.length,
  };
  store.current.educations.push(item);
}

function addSkill() {
  const item: Skill = { name: "", level: 3, order: store.current.skills.length };
  store.current.skills.push(item);
}

async function onSave() {
  const saved = await store.save();
  router.push({ name: "preview", params: { id: saved.id } });
}
</script>

<template>
  <section>
    <h1>{{ resumeId ? "Edit CV" : "New CV" }}</h1>
    <p v-if="store.error" class="error">{{ store.error }}</p>

    <form class="card" @submit.prevent="onSave">
      <h2>Basics</h2>
      <div class="field">
        <label for="title">CV title (for your own reference, not shown to employers)</label>
        <input id="title" v-model="store.current.title" required />
      </div>
      <div class="grid-2">
        <div class="field">
          <label for="full_name">Full name</label>
          <input id="full_name" v-model="store.current.full_name" />
        </div>
        <div class="field">
          <label for="job_title">Target job title</label>
          <input id="job_title" v-model="store.current.job_title" />
        </div>
      </div>
      <div class="grid-2">
        <div class="field">
          <label for="email">Email</label>
          <input id="email" v-model="store.current.email" type="email" />
        </div>
        <div class="field">
          <label for="phone">Phone</label>
          <input id="phone" v-model="store.current.phone" />
        </div>
      </div>
      <div class="field">
        <label for="address">City / address</label>
        <input id="address" v-model="store.current.address" />
      </div>
      <div class="field">
        <label for="summary">Summary</label>
        <textarea id="summary" v-model="store.current.summary" rows="4"></textarea>
      </div>

      <hr />

      <div class="section-head">
        <h2>Work experience</h2>
        <button type="button" class="btn btn-ghost" @click="addExperience">+ Add</button>
      </div>
      <div v-for="(exp, i) in store.current.experiences" :key="i" class="sub-card">
        <div class="grid-2">
          <div class="field">
            <label>Company</label>
            <input v-model="exp.company" />
          </div>
          <div class="field">
            <label>Position</label>
            <input v-model="exp.position" />
          </div>
        </div>
        <div class="grid-3">
          <div class="field">
            <label>Start date</label>
            <input v-model="exp.start_date" type="date" />
          </div>
          <div class="field">
            <label>End date</label>
            <input v-model="exp.end_date" type="date" :disabled="exp.is_current" />
          </div>
          <label class="checkbox-field">
            <input v-model="exp.is_current" type="checkbox" />
            Current job
          </label>
        </div>
        <div class="field">
          <label>Responsibilities / achievements</label>
          <textarea v-model="exp.description" rows="3"></textarea>
        </div>
        <button type="button" class="btn btn-danger" @click="store.current.experiences.splice(i, 1)">
          Remove entry
        </button>
      </div>

      <hr />

      <div class="section-head">
        <h2>Education</h2>
        <button type="button" class="btn btn-ghost" @click="addEducation">+ Add</button>
      </div>
      <div v-for="(edu, i) in store.current.educations" :key="i" class="sub-card">
        <div class="grid-2">
          <div class="field">
            <label>Institution</label>
            <input v-model="edu.institution" />
          </div>
          <div class="field">
            <label>Degree / qualification</label>
            <input v-model="edu.degree" />
          </div>
        </div>
        <div class="field">
          <label>Field of study</label>
          <input v-model="edu.field_of_study" />
        </div>
        <div class="grid-2">
          <div class="field">
            <label>Start date</label>
            <input v-model="edu.start_date" type="date" />
          </div>
          <div class="field">
            <label>End date</label>
            <input v-model="edu.end_date" type="date" />
          </div>
        </div>
        <button type="button" class="btn btn-danger" @click="store.current.educations.splice(i, 1)">
          Remove entry
        </button>
      </div>

      <hr />

      <div class="section-head">
        <h2>Skills</h2>
        <button type="button" class="btn btn-ghost" @click="addSkill">+ Add</button>
      </div>
      <div v-for="(skill, i) in store.current.skills" :key="i" class="skill-row">
        <input v-model="skill.name" placeholder="Skill name" class="skill-name" />
        <input v-model.number="skill.level" type="range" min="1" max="5" />
        <span class="skill-level">{{ skill.level }}/5</span>
        <button type="button" class="btn btn-danger" @click="store.current.skills.splice(i, 1)">×</button>
      </div>

      <div class="save-row">
        <button type="submit" class="btn btn-primary" :disabled="store.isLoading">
          {{ store.isLoading ? "Saving…" : "Save CV" }}
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
h2 {
  font-size: 1.1rem;
  margin-top: 1.5rem;
}

hr {
  border: none;
  border-top: 1px solid var(--line);
  margin: 1.5rem 0;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
  align-items: center;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sub-card {
  background: var(--accent-soft);
  border-radius: var(--radius);
  padding: 1rem;
  margin-bottom: 0.9rem;
}

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--muted);
  white-space: nowrap;
}

.skill-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.6rem;
}

.skill-name {
  flex: 1;
  padding: 0.5rem 0.6rem;
  border: 1px solid var(--line);
  border-radius: var(--radius);
}

.skill-level {
  width: 2.4rem;
  color: var(--muted);
  font-size: 0.85rem;
}

.save-row {
  margin-top: 1.5rem;
}

.error {
  color: var(--danger);
}
</style>
