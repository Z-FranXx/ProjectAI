from django.shortcuts import render,redirect
from .models import User
from .forms import UserForm, AunthenticaUser, UpdateAccountForm
from django.db import IntegrityError
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#view para la creacion de una cuenta
def singup(request):
    
    #Datos recogidos de un formulario
    if request.method == "GET":
        #Renderizar formulario
        return render(request, "login.html",{"form":UserForm()})
    else:
        #Recoger datos del formulario
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            print(userForm.cleaned_data)
            try:
                userForm.save()
            except IntegrityError:
                print("HA OCURRIDO UN ERROR")
                messages.error("Este Correo ya esta siendo utilizado")
                return render(request, 'login.html')
            else:
                email = userForm.cleaned_data['email']
                password = userForm.cleaned_data['password1']
                user = authenticate(request, username=email, password=password)
                login(request, user)
                return redirect("home")
        else:
            
            print("Errores en el formularios ", userForm.errors)

            return render(request, "login.html", {"form":userForm,"welcome":True})


#View para iniciar sesion del usuario
def singin(request):
    if request.method == "GET":
        return render(request, "login.html",{"form":AunthenticaUser()}) 
    else:
        email = request.POST['email']
        password = request.POST['password']
        print(f"Usuario creado {email} {password}\n")
        user = authenticate(request,email=email,password=password)   
        
        if user is None:
            messages.error(request,"El correo electronico o contraseña nos son validos")
            return render(request, "login.html",{"form":AunthenticaUser(),"welcome":True})
        
        login(request,user)
        
        messages.success(request, '¡Has iniciado sesion correctamente!')
        return redirect("home")
    

        
#View para cerrar sesion del usuario
@login_required
def signout(request):
    try:
        logout(request)
    except Exception as e:
        messages.error(request,"No se ha podido cerrar sesion correctamente.")
    else:
        messages.success(request,"¡¡ Has cerrado sesion correctamente !!")
    return redirect('singin')


        