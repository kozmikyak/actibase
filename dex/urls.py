from django.conf.urls import url
from django.views.generic import DetailView
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
#    url(r'^api/$', ListView.as_view(), name="apilist"),
    url(r'^api/searchevents$', SearchEventsAPIView.as_view(), name="detail"),
    url(r'^api/searchpeople$', SearchPeopleAPIView.as_view(), name="detail"),
    url(r'^api/searchpolicy$', SearchPolicyAPIView.as_view(), name="detail"),
    url(r'^api/searchorgs$', SearchOrganizationsAPIView.as_view(), name="detail"),    

    url(r'^api/events$', EventsAPIView.as_view(), name="events"),
    url(r'^api/event/[-@\w]+/$', EventAPIView.as_view(), name="event"),
    url(r'^api/pics/[-@\w]+/$', EventPicsAPIView.as_view(), name="eventpics"),    
    
    url(r'^api/people$', PeopleAPIView.as_view(), name="people"),
    url(r'^api/person/[-@\w]+/$', PersonAPIView.as_view(), name="person"),

    url(r'^api/organizations$', OrgsAPIView.as_view(), name="organizations"),
    url(r'^api/organization/[-@\w]+/$', OrgAPIView.as_view(), name="organization"),    

    url(r'^api/bills$', BillsAPIView.as_view(), name="bills"),
    url(r'^api/bill/[-@\w]+/$', BillAPIView.as_view(), name="bill"),    

    url(r'^api/memberships$', MembershipsAPIView.as_view(), name="memberships"),
    url(r'^api/membership/[-@\w]+/$', MembershipAPIView.as_view(), name="membership"),    

    url(r'^api/posts$', PostsAPIView.as_view(), name="posts"),
    url(r'^api/post/[-@\w]+/$', PostAPIView.as_view(), name="post"),    
]

urlpatterns = format_suffix_patterns(urlpatterns)
