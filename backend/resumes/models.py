from django.db import models


class Resume(models.Model):
    """Top-level CV entity."""

    title = models.CharField("Internal title", max_length=255, default="My CV")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    full_name = models.CharField("Full name", max_length=255, blank=True)
    job_title = models.CharField("Target job title", max_length=255, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Phone", max_length=50, blank=True)
    address = models.CharField("Address / city", max_length=255, blank=True)
    summary = models.TextField("Summary", blank=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "CV"
        verbose_name_plural = "CVs"

    def __str__(self):
        return self.title


class Experience(models.Model):
    """A single work experience entry."""

    resume = models.ForeignKey(Resume, related_name="experiences", on_delete=models.CASCADE)
    company = models.CharField("Company", max_length=255)
    position = models.CharField("Position", max_length=255)
    start_date = models.DateField("Start date", null=True, blank=True)
    end_date = models.DateField("End date", null=True, blank=True)
    is_current = models.BooleanField("Current job", default=False)
    description = models.TextField("Responsibilities / achievements", blank=True)
    order = models.PositiveIntegerField("Order", default=0)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Work experience"
        verbose_name_plural = "Work experience"

    def __str__(self):
        return f"{self.position} @ {self.company}"


class Education(models.Model):
    """A single education entry."""

    resume = models.ForeignKey(Resume, related_name="educations", on_delete=models.CASCADE)
    institution = models.CharField("Institution", max_length=255)
    degree = models.CharField("Degree / qualification", max_length=255, blank=True)
    field_of_study = models.CharField("Field of study", max_length=255, blank=True)
    start_date = models.DateField("Start date", null=True, blank=True)
    end_date = models.DateField("End date", null=True, blank=True)
    order = models.PositiveIntegerField("Order", default=0)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Skill(models.Model):
    """A skill with a proficiency level from 1 to 5."""

    resume = models.ForeignKey(Resume, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField("Skill", max_length=100)
    level = models.PositiveSmallIntegerField("Level (1-5)", default=3)
    order = models.PositiveIntegerField("Order", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name
