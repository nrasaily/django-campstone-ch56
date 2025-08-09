from django.db import models

# Create your models here.
class Note(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()
  created_on = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='media/notes', null=True, blank=True)

  def __str__(self):
    return self.title