from django.db.models import Q
from django.utils.timezone import localtime
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass



class UserFilter(filters.FilterSet):
    office = CharFilterInFilter(field_name='office__location', lookup_expr='in')
    team_leader = CharFilterInFilter(field_name='teamleader__username', lookup_expr='in')