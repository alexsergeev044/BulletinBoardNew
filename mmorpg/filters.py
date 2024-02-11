from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput

from .models import Ads, Response


class AdsFilter(FilterSet):

    date = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d.%m.%Y %H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Ads
        fields = {'category': ['exact'], 'title': ['icontains'], }


class ResponseFilter(FilterSet):

    date = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d.%m.%Y %H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Response
        fields = {'ad': ['exact'], 'accepted': ['exact'], }
