import datetime
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.core.files import File
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.template.loader import get_template
from app_inicial.models import User, Review, Vote_Review, Document
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app_inicial.utils import create_initial_locations
from django.core.files.storage import FileSystemStorage
from rsa import *
import os
#Directorio donde se guardarán los txt
file_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')),"static","texts")

"""
log_in view:
This function handles the log in page.
Args:
    request (HttpRequest)
Returns:
    HttpResponse
"""
def log_in(request):
    if request.method == 'POST':
        nick=request.POST['username']
        contraseña=request.POST['password']
        usuario = authenticate(username=nick, password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/my_documents')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return HttpResponseRedirect('/log_in')
    return render(request,"app_inicial/logIn.html")

"""
log_out view
This function handles the log out page.
Args:
    request
Returns:
    HttpResponse
"""
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/my_documents')


"""
sign_up view: sign up page
Args:
    request
Returns:
    HttpResponse
"""
def sign_up(request):
    if request.method == 'GET':
        return render(request,"app_inicial/signUp.html")
    if request.method=='POST':
        nombre= request.POST['usuario']
        email= request.POST['email']
        contraseña= request.POST['password']
        (pubkey, privkey) = newkeys(1024)
        (pubkey1, pubkey2) = (pubkey.n,pubkey.e)
        (secret_key1, secret_key2, secret_key3, secret_key4, secret_key5) = (privkey.n, privkey.e, privkey.d, privkey.p, privkey.q)
        if User.objects.filter(username=nombre).exists():
            #devolver al mismo login ojalá sin borrar la info ingresada con un mensaje que diga que ya existe ese username
            return render(request,"app_inicial/signUp.html", {"error":"El nombre de usuario '"+nombre+"' ya existe, eliga uno diferente"})
        user = User.objects.create_user(username=nombre, password=contraseña, email=email, public_key1=pubkey1, public_key2=pubkey2)
        login(request, user)
        context = {
            "is_logged": request.user.is_authenticated,
            'secret_key1': secret_key1,
            'secret_key2': secret_key2,
            'secret_key3': secret_key3,
            'secret_key4': secret_key4,
            'secret_key5': secret_key5,
        }
        return render(request,'app_inicial/secret_keys.html', context)
"""
secret_keys view: secret keys page
Args:
    request
Returns:
    HttpResponse
"""
def secret_keys(request):
    if request.method == 'GET':
        return render(request,"/secret_keys.html")
    
"""
Request_to view: here a user can request another user to sign a document.
Args:
    request
Returns:
    HttpResponse
"""
@login_required(login_url='/log_in')
def request_to(request):
    if request.method == 'GET':
        usuarios = User.objects.all()
        context = {
            "is_logged": request.user.is_authenticated,
            'current_page': 'request_to',
            'usuarios': usuarios,
        }
        return render(request,"app_inicial/request_to.html", context)
    if request.method =='POST':
        usuarios = User.objects.all()
        user_id = request.user
        #Contenido del documento
        title = request.POST['title']
        content = request.POST['content']
        if title == '' or content == '':
            context = {
            "is_logged": request.user.is_authenticated,
            'current_page': 'request_to',
            'usuarios': usuarios,
            'content': request.POST['content'],
            'titulo': request.POST['title'],
            }
            if title == '':
                context['error_titulo'] = 'Debe ingresar un título'
            if content == '':
                context['error_content'] = 'Debe ingresar un contenido'
            return render(request,"app_inicial/request_to.html", context)
        
        request_to = User.objects.get(username=request.POST['request_to'])
        fs = FileSystemStorage()
        nombre_archivo= f"{title}.txt"
        ruta_archivo = fs.path(nombre_archivo)
        with open(ruta_archivo, 'w+') as archivo:
            archivo.write(str(content))
            data=archivo.read()
            content_file = ContentFile(data)
            document = Document(
                creator = user_id,
                title = title,
                request_to = request_to, 
                content = content,
                accepted = 0,
                sign = None,
                file_txt=content_file,
                )
            document.save()
            archivo.close()
        context = {
            'current_page': 'request_to',
        }
        return HttpResponseRedirect('/my_documents', context)

"""
Create a document (login required).
This function handles the creation of a document. The user must be logged in to access this view.
Args:
    request (HttpRequest)
Returns:
    HttpResponse or HttpResponseRedirect: The response object.
"""
@login_required(login_url='/log_in')
def create_document(request):
    if request.method == 'GET':
        context = {
            'current_page': 'create_document',
            'is_logged': request.user.is_authenticated,
        }
        return render(request,"app_inicial/create_document.html", context)
    if request.method =='POST':
        user_id = request.user
        #Contenido del documento
        title = request.POST['title']
        content = request.POST['content']
        request_to=request.user
        secret_key1 = request.POST['secret_key1']
        secret_key2 = request.POST['secret_key2']
        secret_key3 = request.POST['secret_key3']
        secret_key4 = request.POST['secret_key4']
        secret_key5 = request.POST['secret_key5']
        try:
            secret_key = PrivateKey(int(secret_key1), int(secret_key2), int(secret_key3), int(secret_key4), int(secret_key5))
        except:
            context={"error":"La llave privada ingresada no es correcta.",
                     "titulo":title,
                     "contenido":content,
                     "is_logged": request.user.is_authenticated,
                     "current_page": "create_document",
                     }
            return render(request,"app_inicial/create_document.html", context)
        fs = FileSystemStorage()
        nombre_archivo= f"{title}.txt"
        ruta_archivo = fs.path(nombre_archivo)
        #Se genera el .txt
        try:
            # Abre el archivo en modo de escritura (w).
            with open(ruta_archivo, 'w') as archivo:
                # Escribe el contenido del string en el archivo.
                archivo.write(str(content))
                archivo.close()
                print(f"Se ha generado el archivo '{title}' correctamente.")
        except IOError:
            print(f"No se pudo generar el archivo '{title}'.")

        try:
            with open(ruta_archivo, 'rb') as file:
                data = file.read()
                signature = sign(data, secret_key, "SHA-256")
                file.close()
            pubkey = PublicKey(int(request.user.public_key1), int(request.user.public_key2))
            #Verifica que la Private Key entregada sea correcta para ese usuario
            verify(data, signature, pubkey)
        except:
            print("error2")
            context={"error":"La llave privada ingresada no es correcta.",
                     "titulo":title,
                     "contenido":content,
                     "is_logged": request.user.is_authenticated,
                     "current_page": "create_document",
                     }
            os.remove(ruta_archivo)
            return render(request,"app_inicial/create_document.html", context)
        #Se guarda el documento en la base de datos
        with open(ruta_archivo, 'r') as archivo:
            data=archivo.read()
            content_file = ContentFile(data)
            #Escribe la firma en el documento
            document = Document(
            creator=user_id, 
            title = title,
            request_to=request_to, 
            content=content,
            accepted=1,
            sign = signature,
            file_txt=content_file,
            )
            document.save()
            archivo.close()
        return HttpResponseRedirect('/my_documents')
    
"""
My Documents (login required).
This function displays the documents of the logged-in user and allows them to see the ones that had been interacted with.
Args:
    request (HttpRequest)
Returns:
    HttpResponse: The response object.
"""
@login_required(login_url='/log_in')
def my_documents(request):
    #Documentos en estado pendiente
    documents = Document.objects.filter(Q(request_to=request.user.id) & Q(accepted=0))
    #Documentos ya resueltos con el usuario como participante
    documentss = Document.objects.filter((Q(creator=request.user.id)|Q(request_to=request.user.id)) & ~Q(accepted=0))
    context = {
        "is_logged": request.user.is_authenticated, 
        "documents": documents,
        "documentss": documentss,
        'current_page': 'my_documents',
    }

    if request.method == 'POST':
        return HttpResponseRedirect('/my_documents', context)

    return render(request, 'app_inicial/my_documents.html', context)

"""
Single document.
This function displays the information of a single document.
Args:
    request (HttpRequest)
    id (int): The id of the document.
Returns:
    HttpResponse: The response object.
""" 
def single_document(request,id):
    context = {
        "is_logged": request.user.is_authenticated,
        
    }
    if not id:
        return HttpResponseRedirect('/my_documents', context)
    document = Document.objects.get(id=id)
    if not document:
        return HttpResponseRedirect('/my_documents', context)

    if request.method == 'GET': 
        context = {
            'is_logged': request.user.is_authenticated,
            'single_document':document, 
            'current_page': 'documents',
        }
        return render(request, 'app_inicial/single_document.html', context)
    
    if request.method == 'POST':
        modify=request.POST['modify']
        if modify=="decline":
            document.accepted = -1
            document.save()
            context = {
                "is_logged": request.user.is_authenticated,
                'current_page': 'documents',
            }
            return HttpResponseRedirect('/my_documents', context)
        
        elif modify=="sign":
            context = {
                "is_logged": request.user.is_authenticated,
                "document": document,
                'current_page': 'documents',
            }
            return HttpResponseRedirect('/sign_document/'+id, context)

"""
Sign document.
This function displays the information of a single document.
Args: 
    request (HttpRequest)
    id (int): The id of the document.
Returns:
    HttpResponse: The response object.
"""
@login_required(login_url='/log_in')
def sign_document(request,id):
    context = {
        "is_logged": request.user.is_authenticated,
    }
    if not id:
        return HttpResponseRedirect('/my_documents', context)
    document = Document.objects.get(id=id)
    if not document:
        return HttpResponseRedirect('/my_documents', context)
    
    if request.method == 'GET':
        context = {
            'current_page': 'sign_document',
            'is_logged': request.user.is_authenticated,
            'document': document,
        }
        return render(request,"app_inicial/sign_document.html", context)
    if request.method =='POST':
        secret_key1 = request.POST['secret_key1']
        secret_key2 = request.POST['secret_key2']
        secret_key3 = request.POST['secret_key3']
        secret_key4 = request.POST['secret_key4']
        secret_key5 = request.POST['secret_key5']
        try:
            secret_key = PrivateKey(int(secret_key1), int(secret_key2), int(secret_key3), int(secret_key4), int(secret_key5))
        except:
            context={"error":"La llave privada ingresada no es correcta.",
                     "is_logged": request.user.is_authenticated,
                     "current_page": "sign_document",
                     }
            return render(request,"app_inicial/sign_document.html", context)
        fs = FileSystemStorage()
        nombre_archivo= f"{document.title}.txt"
        ruta_archivo = fs.path(nombre_archivo)
        try:
            with open(ruta_archivo, 'rb') as file:
                data = file.read()
                signature = sign(data, secret_key, "SHA-256")
                file.close()
            pubkey = PublicKey(int(request.user.public_key1), int(request.user.public_key2))
            #Verifica que la Private Key entregada sea correcta para ese usuario
            verify(data, signature, pubkey)
        except:
            print("error2")
            context={"error":"La llave privada ingresada no es correcta.",
                     "is_logged": request.user.is_authenticated,
                     "current_page": "sign_document",
                     }
            return render(request,"app_inicial/sign_document.html", context)
        #Se guarda el documento en la base de datos
        document.sign = signature
        document.accepted=1
        document.save()
        return HttpResponseRedirect('/my_documents')
"""
download_document: Allows the user to download a pending request.
Args:
    request (HttpRequest)
    doc_id (int): The id of the document.
Returns:
    FileResponse: The response object.
"""
def download_document(request,doc_id):
    document = Document.objects.get(id=doc_id)
    titulo = document.title
    fs = FileSystemStorage()
    nombre_archivo= f"{titulo}.txt"
    ruta_archivo = fs.path(nombre_archivo)
    archivo = open(ruta_archivo, 'rb')
    response = FileResponse(archivo)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(nombre_archivo)
    return response

def verification(request):
    usuarios = User.objects.all()
    if request.method == 'GET':
        context = {
            'current_page': 'verification',
            'usuarios': usuarios,
            'is_logged': request.user.is_authenticated,
        }
        return render(request,"app_inicial/verification.html", context)
    signature=request.POST['signature']
    if request.method =='POST':
        try:
            request_to = User.objects.get(username=request.POST['request_to'])
        except:
            context = {
            'current_page': 'verification',
            'usuarios': usuarios,
            'is_logged': request.user.is_authenticated,
            }
            context['error_usuario'] = 'Debe ingresar un usuario'
            return render(request,"app_inicial/verification.html", context)
        if signature == '':
            context = {
            'current_page': 'verification',
            'usuarios': usuarios,
            'is_logged': request.user.is_authenticated,
            }
            context['error_firma'] = 'Debe ingresar una firma'
            return render(request,"app_inicial/verification.html", context)
        # Manejar el archivo subido
        if 'txtFile' in request.FILES:
            uploaded_file = request.FILES['txtFile']
            # Utilizar una carpeta temporal para almacenar los archivos
            temp_storage = FileSystemStorage(location='temp_uploads')
            filename = temp_storage.save(uploaded_file.name, uploaded_file)
            file_path = temp_storage.path(filename)
            request_to = User.objects.get(username=request.POST['request_to'])
            # Procesar el archivo (ejemplo: leer su contenido)
            with temp_storage.open(file_path, 'rb') as file:
                try:
                    file_content = file.read().decode('utf-8')
                    Document.objects.get(request_to=request_to, sign=signature, content=file_content)
                    file.close()
                    temp_storage.delete(filename)
                except:
                    context = {
                        'current_page': 'verification',
                        'usuarios': usuarios,
                        'is_logged': request.user.is_authenticated,
                    }
                    context['error_firma'] = 'La firma no es válida'
                    file.close()
                    temp_storage.delete(filename)
                    return render(request,"app_inicial/verification.html", context)
            context = {
                'current_page': 'verification',
                'usuarios': usuarios,
                'is_logged': request.user.is_authenticated,
            }
            context['success'] = 'La firma es válida'
            return render(request,"app_inicial/verification.html", context)
        else:
            context = {
                'current_page': 'verification',
                'usuarios': usuarios,
                'is_logged': request.user.is_authenticated,
            }
            context['error_archivo'] = 'Debe ingresar un archivo'
            return render(request,"app_inicial/verification.html", context)