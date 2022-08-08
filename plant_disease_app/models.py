from django.db import models
from django.contrib.auth.models import User

disease=('Soybean___healthy','Squash___Powdery_mildew','Strawberry___Leaf_scorch','Strawberry___healthy','Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot','Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy')
# Create your models here.


class photo_model(models.Model):
    photo = models.ImageField(upload_to='Images')


class Predicted_label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ForeignKey('Image_stored',on_delete=models.CASCADE, null=True, blank=True)
    label=models.CharField(max_length=50, null=True, blank=True)


class Image_stored(models.Model):
    photo = models.ImageField(upload_to='Pred')