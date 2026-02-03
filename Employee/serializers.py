from rest_framework import serializers
from .models import (Employee,Developer,HR,Interview,Candidate)



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class HRSerailizer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = '__all__'
        read_only_fields = ['department','internal_notes']     

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'
        read_only_fields = ['department',]

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'                   

class InterviewSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    
    interviwers = EmployeeSerializer(many=True,read_only=True)

    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(),
        source = 'candidate',
        write_only = True
    )
    interviewer_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Employee.objects.all(),
         source="interviwers",
        write_only=True
    )     

    class Meta:
        model = Interview
        fields = "__all__" 
        read_only_fields = ["id", "candidate", "interviwers",'status']


    def create(self,validated_data):
        print("create...")
        breakpoint()
        candidate = validated_data.pop("candidate")
        interviwers = validated_data.pop("interviwers")
        
        interview = Interview.objects.create(
            candidate=candidate,
            **validated_data
        )
        interview.interviwers.set(interviwers)
        return interview

  