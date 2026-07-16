from rest_framework import viewsets

from .models import Resume
from .serializers import ResumeListSerializer, ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    """CRUD for CVs.

    list  -> lightweight version (no nested lists)
    detail/create/update -> full version with experience, education and skills
    """

    queryset = Resume.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ResumeListSerializer
        return ResumeSerializer
