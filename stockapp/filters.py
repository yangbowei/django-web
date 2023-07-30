from django.db.models import Q
import django_filters
from . import models


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = models.Product
        fields = ['q']

    def universal_search(self, queryset, name, value):
        return models.Product.objects.filter(
            Q(brand__icontains=value) | Q(model__icontains=value) | Q(source__icontains=value)
        )
