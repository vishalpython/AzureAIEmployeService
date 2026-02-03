from django.urls import include,path
#import debug_toolbar
from .views import DeveloperViewSet,EmployeeViewSet,InterviewViewset,CandidateViewsets,HRViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'hrs',HRViewSets)
router.register(r'developers',DeveloperViewSet)
router.register(r'employees',EmployeeViewSet,basename='employee')
router.register(r'candidates',CandidateViewsets)
router.register(r'interviews',InterviewViewset)

#
urlpatterns =[
    path('api/',include(router.urls)),
]

