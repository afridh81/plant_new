from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import numpy as np
import os
from .models import *
from django.http import HttpResponse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import os, shutil
from django.core.mail import send_mail
from plant_disease_project import settings
# Machine Learning Packages
# from django.conf import settings
# Create your views here.

@login_required(login_url='login-h')
def home(request):
    return render(request, 'index.html')


def loginpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        except:
            messages.warning("Fill the details")
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login-h')
    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login-h')
def move():
    path = os.getcwd()+"/media/Images/"
    moveto = os.getcwd()+"/media/Pred/"
    files = os.listdir(path)
    print(files)
    files.sort()
    for f in files:
        src = path + f
        dst = moveto + f
        shutil.move(src, dst)

def photo_store(request):
    if request.method == 'POST':
        photo_model.objects.all().delete()
        form = photo_forms(request.POST, request.FILES)
        print(os.getcwd())
        pestiside = ""
        dir = os.getcwd()+'/media/Images'
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                print(path)
                os.remove(path)
        if form.is_valid():
            form.save()
            new_model = tf.keras.models.load_model('data/plant_disease.h5')
            path = os.getcwd()+'/media/Images'
            for root, dirs, files in os.walk(dir):
                for file in files:
                    path = os.path.join(dir, file)
                    print(path)
            img_width, img_height = 224, 224
            img = image.load_img(path, target_size=(img_width, img_height))
            out = np.expand_dims(img, axis=0)
            final_img = out / 255.0

            pred = new_model.predict(final_img)
            max_index = np.argmax(pred[0])
            print(max_index)
            values = ('Soybean___healthy','Squash___Powdery_mildew','Strawberry___Leaf_scorch','Strawberry___healthy','Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot','Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato__Healthy')
            predicted = values[max_index]
            print(pred[0])
            print(predicted)

            send_mail_plant(request.user.username,predicted,request.user.email)

            phot = photo_model.objects.last()
            move()
            Image_stored.objects.create(photo =phot.photo.url )
            user_now = User.objects.get(username=request.user)
            imag = Image_stored.objects.last()
            Predicted_label.objects.create(user=user_now,photo=imag,label=predicted)
            if predicted=="Strawberry___Leaf_scorch":
                pestiside="Avoiding sprinkler irrigation and cull piles near greenhouse or field operations, and rotating with a nonhost crop also helps control the disease"

            elif predicted=="Tomato___Bacterial_spot":
                pestiside="Cultural practices and preventive sprays of copper help to manage bacterial spot"



            elif predicted=="Squash___Powdery_mildew":
                pestiside="A better treatment solution for your squash plants is baking soda. "

            elif predicted=="Tomato___Early_blight" or predicted=="Tomato___Late_blight":
                pestiside=" Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable. Both of these treatments are organic."

            elif predicted == "Tomato___Leaf_Mold" or predicted == "Tomato___Septoria_leaf_spot" or predicted == "Tomato___Spider_mites Two-spotted_spider_mite" or predicted == "Tomato___Target_Spot" or predicted == "Tomato___Tomato_Yellow_Leaf_Curl_Virus" or predicted == "Tomato___Tomato_mosaic_virus":
                pestiside = "Contact insecticides such as bifenthrin, cypermethrin, cyhalothrin, permethrin, and esfenvalerateare effective in controllin bugs, leaf - footed bugs, aphids, fruitworms, and hornworms"


            else:
                pestiside="Healthy"

            print(request.user,'----------user')
            print(phot.photo.url)
            phot.delete()
            return render(request, 'urls.html', {'msg': predicted, 'photo': phot,'url':phot.photo.url,'pestiside':pestiside})
    else:
        form = photo_forms()
    return render(request, 'photo.html', {'form': form})



def check(request):
    return render(request, 'urls.html')



def send_mail_plant(name,disease,email):
    from django.template.loader import get_template
    from django.core.mail import EmailMultiAlternatives
    htmly = get_template('email.html')
    subject = 'Plant Disease'
    to =email

    try:
        html_content = htmly.render({
            'disease': disease,
            'name': name,

        })
        print(name)
        print(disease)

        msg = EmailMultiAlternatives(subject, subject, settings.EMAIL_HOST_USER, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('mail send --------')
        status = True
    except Exception as e:
        status = False
        print(e,'--------------exceptions')
    print(status,'-----------status')
    return status