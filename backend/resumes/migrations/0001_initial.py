from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="My CV", max_length=255, verbose_name="Internal title")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(blank=True, max_length=255, verbose_name="Full name")),
                ("job_title", models.CharField(blank=True, max_length=255, verbose_name="Target job title")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Phone")),
                ("address", models.CharField(blank=True, max_length=255, verbose_name="Address / city")),
                ("summary", models.TextField(blank=True, verbose_name="Summary")),
            ],
            options={
                "verbose_name": "CV",
                "verbose_name_plural": "CVs",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company", models.CharField(max_length=255, verbose_name="Company")),
                ("position", models.CharField(max_length=255, verbose_name="Position")),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="Start date")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="End date")),
                ("is_current", models.BooleanField(default=False, verbose_name="Current job")),
                ("description", models.TextField(blank=True, verbose_name="Responsibilities / achievements")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                ("resume", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="experiences", to="resumes.resume")),
            ],
            options={
                "verbose_name": "Work experience",
                "verbose_name_plural": "Work experience",
                "ordering": ["order", "-start_date"],
            },
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("institution", models.CharField(max_length=255, verbose_name="Institution")),
                ("degree", models.CharField(blank=True, max_length=255, verbose_name="Degree / qualification")),
                ("field_of_study", models.CharField(blank=True, max_length=255, verbose_name="Field of study")),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="Start date")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="End date")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                ("resume", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="educations", to="resumes.resume")),
            ],
            options={
                "verbose_name": "Education",
                "verbose_name_plural": "Education",
                "ordering": ["order", "-start_date"],
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Skill")),
                ("level", models.PositiveSmallIntegerField(default=3, verbose_name="Level (1-5)")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                ("resume", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skills", to="resumes.resume")),
            ],
            options={
                "verbose_name": "Skill",
                "verbose_name_plural": "Skills",
                "ordering": ["order"],
            },
        ),
    ]
