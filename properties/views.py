from rest_framework import viewsets

from properties import serializers
from properties import models


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Property model """
    queryset = models.Property.objects.filter(active=True)
    serializer_class = serializers.PropertySerializer
    
    def get_queryset(self):
        """ filter with get parameters """
        queryset = models.Property.objects.filter(active=True)
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            queryset = queryset.filter(featured=True)
            
        # return queryset
        return queryset