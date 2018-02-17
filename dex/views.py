from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from django.db.models import Q

from cities.models import City
from dex.models.dx_cities import dx_City

from opencivicdata.core.models import Person, Organization, Membership, Post
from opencivicdata.legislative.models import Event, Bill

from .serializers import (
    OrganizationsSerializer,
    OrgSerializer,    
    PersonSerializer,
    PostSerializer,
    MembershipSerializer,    
    PeopleSerializer,    
    EventSerializer,
    BillSerializer
    )

from rest_framework.settings import api_settings
from rest_framework import generics

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


############
## Events ##
############
@permission_classes([])
@authentication_classes([])
class EventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(start_date__gte=datetime.now())
    queryset = queryset.order_by('start_date')


@permission_classes([])
@authentication_classes([])
class EventAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        path = 'ocd-event/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Event.objects.filter(id=path)
        return queryset

@permission_classes([])
@authentication_classes([])
class EventPicsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        path = self.request.path.split('/')[-2].replace('-', ' ')
        queryset = Event.objects.filter(start_date__gte=datetime.now(), jurisdiction__name=path)
        return queryset.order_by('start_date')
    

#################
## Memberships ##
#################
@permission_classes([])
@authentication_classes([])
class MembershipsAPIView(generics.ListAPIView):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        path = 'ocd-person/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Membership.objects.filter(person__id=path)
        return queryset


@permission_classes([])
@authentication_classes([])
class MembershipAPIView(generics.ListAPIView):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        path = 'ocd-person/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Membership.objects.filter(id=path)
        return queryset

    
###########
## Posts ##
###########
@permission_classes([])
@authentication_classes([])
class PostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        path = 'ocd-organization/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Post.objects.filter(organization__id=path)
        return queryset

    
@permission_classes([])
@authentication_classes([])
class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        path = 'ocd-post/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Post.objects.filter(id=path)
        return queryset
    
    
###################
## Organizations ##
###################
@permission_classes([])
@authentication_classes([])
class OrgsAPIView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationsSerializer


@permission_classes([])
@authentication_classes([])
class OrgAPIView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer

    def get_queryset(self):
        path = 'ocd-organization/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Organization.objects.filter(id=path)
        return queryset


############
## People ##
############
@permission_classes([])
@authentication_classes([])
class PeopleAPIView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PeopleSerializer

    
@permission_classes([])
@authentication_classes([])
class PersonAPIView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        path = 'ocd-person/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Person.objects.filter(id=path)
        return queryset

    
############
## Policy ##
############
@permission_classes([])
@authentication_classes([])
class BillsAPIView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


@permission_classes([])
@authentication_classes([])
class BillAPIView(generics.ListAPIView):
    serializer_class = BillSerializer

    def get_queryset(self):
        path = 'ocd-bill/' + self.request.path.split('/')[-2]
        print(path)
        queryset = Bill.objects.filter(id=path)
        return queryset

    
###################
## Search Events ##
###################
@permission_classes([])
@authentication_classes([])
class SearchEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        event_query = self.request.query_params.get('q', None)
        if event_query is not None:
            queryset = queryset.filter(
                Q(name__icontains=event_query)|
                Q(description__icontains=event_query)|
                Q(jurisdiction__name__icontains=event_query)                
            ).distinct()
        return queryset


###################
## Search People ##
###################
@permission_classes([])
@authentication_classes([])
class SearchPeopleAPIView(generics.ListAPIView):
    serializer_class = PeopleSerializer

    def get_queryset(self):
        queryset = Person.objects.all()
        ppl_query = self.request.query_params.get('q', None)
        if ppl_query is not None:
            queryset = queryset.filter(
                Q(name__icontains=ppl_query)
            ).distinct()
        return queryset


##################
## Search Bills ##
##################
@permission_classes([])
@authentication_classes([])
class SearchPolicyAPIView(generics.ListAPIView):
    serializer_class = BillSerializer

    def get_queryset(self):
        queryset = Bill.objects.all()
        bill_query = self.request.query_params.get('q', None)
        if bill_query is not None:
            queryset = queryset.filter(
                Q(identifier__icontains=bill_query)|
                Q(title__icontains=bill_query)
            ).distinct()
        return queryset


##########################
## Search Organizations ##
##########################
@permission_classes([])
@authentication_classes([])
class SearchOrganizationsAPIView(generics.ListAPIView):
    serializer_class = OrganizationsSerializer

    def get_queryset(self):
        queryset = Organization.objects.all()
        org_query = self.request.query_params.get('q', None)
        if org_query is not None:
            queryset = queryset.filter(Q(name__icontains=org_query)).distinct()
            print(org_query)
        return queryset



