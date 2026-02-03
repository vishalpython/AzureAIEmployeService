from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class TimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampModel):

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True    


class Employee(Person):
    DEPT_CHOICES = (
        ("HR","Human Resource"),
        ("ENG","Engneer"),
        ("MGR","Manager")
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,    # default: auth.User
        on_delete=models.CASCADE,
        related_name="employee_profile",
        null=True,
        blank=True,
    )
    department = models.CharField(max_length=220,choices=DEPT_CHOICES)

    salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)]
    )
    performance_score = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

class HR(Employee):
    """
    HR Employee - Manage the candidate and sheduling interview
    """    
    region = models.CharField(max_length=20)
    internal_notes = models.JSONField(default=dict,blank=True)

    class Meta:
        verbose_name = 'HR'
        verbose_name_plural = 'HRs'
    
    def save(self,*args,**kwargs):
        self.department = 'HR'
        print("####################### HR")
        super().save(*args,**kwargs)

    def add_internal_note(self,candidate_id,note):
        notes_for_candidate = self.internal_notes.get(str(candidate_id), [])
        notes_for_candidate.append(note)
        self.internal_notes[str(candidate_id)] = notes_for_candidate
        self.save(update_fields=["internal_notes"])


class Developer(Employee):
    primary_skill = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'

    def save(self,*args,**kwargs):
        print(f'DEveloper.....:{self.department}')
        self.department = 'ENG'
        super().save(*args,**kwargs) 

    def evaluate_candidate_technical(self, candidate: "Candidate") -> dict:
        tech_match = self.primary_skill in candidate.skills
        score = 4 if tech_match else 2
        return {
            "technical_match": tech_match,
            "score": score,
            "comments": "Strong technical skills" if tech_match else "Needs improvement",
        }       

class Candidate(Person):
    skills = models.JSONField(default=dict,blank=True)
    year_of_exprience = models.PositiveIntegerField(default=0)



class Interview(TimeStampModel):
    STATUS =( ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled")
    )    

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interviwers = models.ManyToManyField(Employee, )

    sheduled_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20,choices=STATUS,default='SCHEDULED')


