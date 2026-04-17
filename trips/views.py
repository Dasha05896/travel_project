from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import TravelProject, Place
from .serializers import TravelProjectSerializer, PlaceSerializer


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all()
    serializer_class = TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete project because it contains visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_update(self, serializer):
        serializer.save()


        place = serializer.instance
        project = place.project


        if not project.places.filter(is_visited=False).exists():
            project.is_completed = True
            project.save()