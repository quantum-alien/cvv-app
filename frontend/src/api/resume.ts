import { apiClient } from "./client";
import type { Resume, ResumeListItem } from "@/types/resume";

export const resumeApi = {
  async list(): Promise<ResumeListItem[]> {
    const { data } = await apiClient.get("resumes/");
    // DRF pagination wraps the result in { results: [...] }
    return Array.isArray(data) ? data : data.results;
  },

  async get(id: number): Promise<Resume> {
    const { data } = await apiClient.get(`resumes/${id}/`);
    return data;
  },

  async create(resume: Resume): Promise<Resume> {
    const { data } = await apiClient.post("resumes/", resume);
    return data;
  },

  async update(id: number, resume: Resume): Promise<Resume> {
    const { data } = await apiClient.put(`resumes/${id}/`, resume);
    return data;
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`resumes/${id}/`);
  },
};
