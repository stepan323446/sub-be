import requests
from urllib.parse import urlparse
from django.db import models
from django.core.files.base import ContentFile

from users.models import User

# Create your models here.
class Service(models.Model):
    name        = models.CharField(max_length=50)
    url         = models.CharField(max_length=255, null=True, blank=True)
    icon        = models.ImageField(upload_to='service-icons/', null=True)
    
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def download_icon_website(self):
        if not self.url:
            return False
        
        parsed = urlparse(self.url if self.url.startswith("http") else "https://" + self.url)
        domain = parsed.netloc
        favicon_url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"

        response = requests.get(favicon_url)
        if response.status_code == 200:
            file_name = f"{domain}.png"
            self.icon.save(file_name, ContentFile(response.content), save=False)
            return True
        
        return False
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = Service.objects.get(pk=self.pk)
            if old and old.url != self.url and self.url:
                self.download_icon_website()
        elif self.url:
            self.download_icon_website()

        super().save(*args, **kwargs)