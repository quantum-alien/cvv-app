from rest_framework import serializers

from .models import Education, Experience, Resume, Skill


class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Experience
        fields = [
            "id", "company", "position", "start_date", "end_date",
            "is_current", "description", "order",
        ]


class EducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Education
        fields = [
            "id", "institution", "degree", "field_of_study",
            "start_date", "end_date", "order",
        ]


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ["id", "name", "level", "order"]


class ResumeSerializer(serializers.ModelSerializer):
    """Full CV: personal info + nested experience/education/skills lists.

    Supports nested writes (create/update) so the frontend can save the
    whole CV in a single PUT request.
    """

    experiences = ExperienceSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = [
            "id", "title", "created_at", "updated_at",
            "full_name", "job_title", "email", "phone", "address", "summary",
            "experiences", "educations", "skills",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        experiences_data = validated_data.pop("experiences", [])
        educations_data = validated_data.pop("educations", [])
        skills_data = validated_data.pop("skills", [])

        resume = Resume.objects.create(**validated_data)
        self._sync_children(resume, experiences_data, educations_data, skills_data)
        return resume

    def update(self, instance, validated_data):
        experiences_data = validated_data.pop("experiences", None)
        educations_data = validated_data.pop("educations", None)
        skills_data = validated_data.pop("skills", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._sync_children(instance, experiences_data, educations_data, skills_data)
        return instance

    @staticmethod
    def _sync_children(resume, experiences_data, educations_data, skills_data):
        # Simple "replace all" strategy: delete existing rows and recreate
        # them from the submitted data. That's enough for a CV form where
        # the user edits the whole list at once.
        if experiences_data is not None:
            resume.experiences.all().delete()
            for item in experiences_data:
                item.pop("id", None)
                Experience.objects.create(resume=resume, **item)

        if educations_data is not None:
            resume.educations.all().delete()
            for item in educations_data:
                item.pop("id", None)
                Education.objects.create(resume=resume, **item)

        if skills_data is not None:
            resume.skills.all().delete()
            for item in skills_data:
                item.pop("id", None)
                Skill.objects.create(resume=resume, **item)


class ResumeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for the CV list (no nested lists)."""

    class Meta:
        model = Resume
        fields = ["id", "title", "full_name", "job_title", "updated_at"]
