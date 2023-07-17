import datetime
from django.core.exceptions import ValidationError
from django.core.files import File
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.template.loader import get_template
from app_inicial.models import User, Review, Vote_Review, Document
from django.http import HttpResponse, HttpResponseRedirect
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
Manage vote for a review.
This function handles operations related to voting on a review.
It updates the vote count and the user's voting record.
Args:
    request (HttpRequest)
    kind (int): The type of vote: -1 for negative vote, 1 for positive vote.
Returns:
    None
"""
def manageVote(request,kind):
    if request.user.is_authenticated:
        review_id=request.POST['review-id']
        review=Review.objects.get(id=review_id)
        #si existia
        if Vote_Review.objects.filter(user_id=request.user, review_id=review_id).exists():
            hasVoted=Vote_Review.objects.get(user_id=request.user, review_id=review_id)
        #si no existia
        else:
            hasVoted=Vote_Review(
                user=request.user,
                review=review,
                is_positive=0
                )
            
        #si es 0 -> deberia sumar 1
        if hasVoted.is_positive == 0:
            review.votes+=kind
            review.total_votes+=1
            hasVoted.is_positive=kind
            hasVoted.save()
            review.save()
            return
        
        #si es el contrario de antes -> deberia sumar 2
        if hasVoted.is_positive != kind:                
            review.votes+=2*kind
            review.total_votes+=1
            hasVoted.is_positive=kind
            hasVoted.save()
            review.save()
            return
        
        #si es el mismo de antes -> deberia restar 1
        else:
            review.votes-=kind
            review.total_votes-=1
            hasVoted.is_positive=0
            hasVoted.save()
            review.save()
            return

"""
Delete
Maintain votes for a list of reviews.
This function updates the vote status for each review in the given list, based on the user's voting record.
Args:
    request (HttpRequest)
    allReviews (list): A list of review IDs.
Returns:
    None
"""
def mantainVotes(request,allReviews):
    for r in allReviews:
        if Vote_Review.objects.filter(user_id=request.user, review_id=r).exists():
            r.isPositive=Vote_Review.objects.get(review=r,user=request.user).is_positive
            
"""
Home view
This function handles the home page.
Args:
    request (HttpRequest)
Returns:
    HttpResponse
"""
def home(request):
    is_logged = request.user.is_authenticated
    best_reviews = Review.objects.order_by('-votes')[:3]
    best_review = best_reviews[0] if len(best_reviews) > 0 else None
    second_best_review = best_reviews[1] if len(best_reviews) > 1 else None
    third_best_review = best_reviews[2] if len(best_reviews) > 2 else None
    if is_logged:
        if Vote_Review.objects.filter(user_id=request.user, review_id=best_review).exists():
                best_review.isPositive=Vote_Review.objects.get(review=best_review,user=request.user).is_positive
    context = {
        'is_logged': is_logged,
        'current_page': 'home',
        'best_review': best_review,	
        'second_best_review': second_best_review,
        'third_best_review': third_best_review,
    }
    if request.method == 'POST':
        modify=request.POST['modify']
        if modify=='upvote':
            manageVote(request,1)
        if modify=='downvote':
            manageVote(request,-1)
        return HttpResponseRedirect('/home', context)
    return render(request, 'app_inicial/home.html', context)
    

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
            return HttpResponseRedirect('/home')
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
    return HttpResponseRedirect('/home')


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

def secret_keys(request):
    if request.method == 'GET':
        return render(request,"/secret_keys.html")
"""
Add a review (login required).
This function handles the addition of a review. The user must be logged in to access this view.
Args:
    request (HttpRequest)
Returns:
    HttpResponse or HttpResponseRedirect: The response object.
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
        nombre_archivo= f"{title}1.txt"
        ruta_archivo = fs.path(nombre_archivo)
        with open(ruta_archivo, 'w+') as archivo:
            archivo.write(str(content))
            document = Document(
                creator = user_id,
                title = title,
                request_to = request_to, 
                content = content,
                accepted = 0,
                sign = None,
                file_txt=File(archivo, name=f"{title}.txt"),
                )
            document.save()
            archivo.close()
            os.remove(ruta_archivo)
        context = {
            'current_page': 'request_to',
        }
        return HttpResponseRedirect('/home', context)

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
        nombre_archivo= f"{title}1.txt"
        ruta_archivo = fs.path(nombre_archivo)
        #Se genera el .txt
        try:
            # Abre el archivo en modo de escritura (w).
            with open(ruta_archivo, 'w') as archivo:
                # Escribe el contenido del string en el archivo.
                archivo.write(str(content))
                archivo.close()
                print(f"Se ha generado el archivo '{title}1' correctamente.")
        except IOError:
            print(f"No se pudo generar el archivo '{title}1'.")

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
        with open(ruta_archivo, 'a+') as archivo:
            #Escribe la firma en el documento
            document = Document(
            creator=user_id, 
            title = title,
            request_to=request_to, 
            content=content,
            accepted=1,
            sign = signature,
            file_txt=File(archivo, name=f"{title}.txt"),
            )
            document.save()
            archivo.close()
            #Se elimina el archivo original, dejando la copia con el nombre sin el número 1
            os.remove(ruta_archivo)
        return HttpResponseRedirect('/home')
    
"""
My reviews (login required).
This function displays the reviews of the logged-in user and allows them to modify the reviews by voting on them.
Args:
    request (HttpRequest)
Returns:
    HttpResponse: The response object.
"""
@login_required(login_url='/log_in')
def my_documents(request):
    documents = Document.objects.filter(creator=request.user.id)
    
    context = {
        "is_logged": request.user.is_authenticated, 
        "documents": documents,
        'current_page': 'my_documents',
    }

    if request.method == 'POST':
        return HttpResponseRedirect('/my_documents', context)

    return render(request, 'app_inicial/my_documents.html', context)

"""
Reviews.
This function displays the available reviews and allows users to search, filter, and modify them.
Args:
    request (HttpRequest)
Returns:
    HttpResponse: The response object.
"""
def reviews(request):
    is_logged = request.user.is_authenticated
    queryset = Review.objects.all()
    order = request.GET.get('order')
    venueFilter = request.GET.get('venueFilter', '')
    if venueFilter:
        queryset = queryset.filter(venue__name=venueFilter)
    if order == 'recent':
        queryset = queryset.order_by('-date')
    elif order == 'oldest':
        queryset = queryset.order_by('date')
    elif order == 'best':
        queryset = queryset.order_by('-votes')
    elif order == 'popular':
        queryset = queryset.order_by('-total_votes')
    reviews = queryset.all()

    if is_logged:
        mantainVotes(request,reviews)

    context = {
        'is_logged': is_logged,
        'all_reviews': reviews,
        'current_page': 'reviews',	
    }
    # Search review by artist or event
    concert = request.GET.get('searchReview')
    if concert:
        context['all_reviews'] = Review.objects.filter(concert__icontains=concert)

    if request.method == 'POST':
        modify=request.POST['modify']
        if modify=='upvote':
            manageVote(request,1)
        if modify=='downvote':
            manageVote(request,-1)
        return HttpResponseRedirect('/reviews', context)
      
    return render(request, 'app_inicial/reviews.html', context)

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
        return HttpResponseRedirect('/home', context)
    
    document = Document.objects.get(id=id)
    if not document:
        return HttpResponseRedirect('/home', context)

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
            return HttpResponseRedirect('/home', context)
        
        elif modify=="sign":
            context = {
                "is_logged": request.user.is_authenticated,
                "document": document,
                'current_page': 'documents',
            }
            return HttpResponseRedirect('/sign_document/'+id, context)

def sign_document(request):
    return
