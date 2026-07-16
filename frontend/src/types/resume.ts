export interface Experience {
  id?: number;
  company: string;
  position: string;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
  description: string;
  order: number;
}

export interface Education {
  id?: number;
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string | null;
  end_date: string | null;
  order: number;
}

export interface Skill {
  id?: number;
  name: string;
  level: number; // 1-5
  order: number;
}

export interface Resume {
  id?: number;
  title: string;
  created_at?: string;
  updated_at?: string;
  full_name: string;
  job_title: string;
  email: string;
  phone: string;
  address: string;
  summary: string;
  experiences: Experience[];
  educations: Education[];
  skills: Skill[];
}

export interface ResumeListItem {
  id: number;
  title: string;
  full_name: string;
  job_title: string;
  updated_at: string;
}

export function emptyResume(): Resume {
  return {
    title: "My CV",
    full_name: "",
    job_title: "",
    email: "",
    phone: "",
    address: "",
    summary: "",
    experiences: [],
    educations: [],
    skills: [],
  };
}
