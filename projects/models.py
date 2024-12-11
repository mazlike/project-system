from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)

    def __str__(self):
        return self.title

    def assign_leader(self, user):
        self.leader = user
        self.save()

    def add_member(self, user):
        self.members.add(user)
        self.save()

class Repository(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.project.title} Repository"
    
class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('leader', 'Leader')], default='pending')

    def __str__(self):
        return f"{self.applicant.username} -> {self.project.title}"