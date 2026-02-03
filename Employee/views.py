from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Employee,Candidate,HR,Developer,Interview
from .authentications import ExpiringAuthentication
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import EmployeeSerializer,CandidateSerializer,HRSerailizer,InterviewSerializer,DeveloperSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "refresh token required"}, status=400)
        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    
class HRViewSets(viewsets.ModelViewSet):
    queryset = HR.objects.all()
    serializer_class = HRSerailizer
    #authentication_classes = [ExpiringAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self,request,*args,**kwargs):
         user_key = f"user_{request.user.id}_hr_list_count"
         count = request.session.get('hr_list_count',0)
         cache_count = cache.get(user_key,0)
         cache_count+=1
         count+=1
         request.session['hr_list_count'] = count
         cache.set(user_key,cache_count,timeout=60)
         response = super().list(request,*args,**kwargs)
         response.data = {
            'api_call_count_this_session': count,
            'api_cache_count':cache_count,
            'results': response.data
            }
         
         return response
    



class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class CandidateViewsets(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer 
 
    @action(detail=True, methods=['post'])
    def shedule_interview(self, request,pk=None):
        candidate = self.get_object()
        hr_id = request.data.get("hr_id")
        interviewer_ids = request.data.get("interviewer_ids", [])     
        try:
            hr = HR.objects.get(pk=hr_id)
        except HR.DoesNotExist:
            return Response({"detail": "Invalid hr_id"}, status=status.HTTP_400_BAD_REQUEST)

        # optional note from HR
        note = request.data.get("note")
        if note:
            hr.add_internal_note(candidate.id, note) 

        # Build serializer-style payload for InterviewSerializer.create
        payload = {
            "candidate_id": candidate.id,
            "interviewer_ids": interviewer_ids,
            "scheduled_at": request.data.get("scheduled_at"),
            "location": request.data.get("location"),
        }
        breakpoint()
        serializer = InterviewSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        interview = serializer.save()

        return Response(
            InterviewSerializer(interview).data,
            status=status.HTTP_201_CREATED
        )
    

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
        """
        Read-only viewset just to list all employees,
        regardless of specific subclass.
        """
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer

class InterviewViewset(viewsets.ModelViewSet):
     queryset  = Interview.objects.all().select_related("candidate").prefetch_related("interviwers")  
     serializer_class = InterviewSerializer      




