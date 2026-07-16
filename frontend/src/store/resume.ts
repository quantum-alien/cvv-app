import { defineStore } from "pinia";
import { resumeApi } from "@/api/resume";
import { emptyResume, type Resume, type ResumeListItem } from "@/types/resume";

export const useResumeStore = defineStore("resume", {
  state: () => ({
    list: [] as ResumeListItem[],
    current: emptyResume() as Resume,
    isLoading: false,
    error: "" as string,
  }),

  actions: {
    async fetchList() {
      this.isLoading = true;
      this.error = "";
      try {
        this.list = await resumeApi.list();
      } catch (e) {
        this.error = "Failed to load the CV list";
      } finally {
        this.isLoading = false;
      }
    },

    async fetchOne(id: number) {
      this.isLoading = true;
      this.error = "";
      try {
        this.current = await resumeApi.get(id);
      } catch (e) {
        this.error = "Failed to load the CV";
      } finally {
        this.isLoading = false;
      }
    },

    startNew() {
      this.current = emptyResume();
    },

    async save(): Promise<Resume> {
      this.isLoading = true;
      this.error = "";
      try {
        if (this.current.id) {
          this.current = await resumeApi.update(this.current.id, this.current);
        } else {
          this.current = await resumeApi.create(this.current);
        }
        return this.current;
      } catch (e) {
        this.error = "Failed to save the CV. Please check the fields you filled in.";
        throw e;
      } finally {
        this.isLoading = false;
      }
    },

    async remove(id: number) {
      await resumeApi.remove(id);
      this.list = this.list.filter((r) => r.id !== id);
    },
  },
});
