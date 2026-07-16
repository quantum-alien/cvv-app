import { createRouter, createWebHistory } from "vue-router";
import ResumeListView from "@/views/ResumeListView.vue";
import ResumeEditView from "@/views/ResumeEditView.vue";
import ResumePreviewView from "@/views/ResumePreviewView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "list", component: ResumeListView },
    { path: "/resumes/new", name: "new", component: ResumeEditView },
    { path: "/resumes/:id/edit", name: "edit", component: ResumeEditView, props: true },
    { path: "/resumes/:id/preview", name: "preview", component: ResumePreviewView, props: true },
  ],
});

export default router;
