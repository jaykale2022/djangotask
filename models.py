from django.db import models
 
class UploadedFile(models.Model):
   name =models.CharField(max_length=100)
   file= models.FileField(upload_to='uploads/')
   uploaded_at= models.DateTimeField(auto_now_add=True)
   
    
   
