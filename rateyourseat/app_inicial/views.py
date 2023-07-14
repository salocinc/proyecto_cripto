import datetime
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.template.loader import get_template
from app_inicial.models import User, Review, Location, ReviewForm, Comment, Vote_Review, Document
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app_inicial.utils import create_initial_locations
from rsa import sign, verify, newkeys

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
        if User.objects.filter(username=nombre).exists():
            #devolver al mismo login ojalá sin borrar la info ingresada con un mensaje que diga que ya existe ese username
            return render(request,"app_inicial/signUp.html", {"error":"El nombre de usario '"+nombre+"' ya existe, eliga uno diferente"})
        user = User.objects.create_user(username=nombre, password=contraseña, email=email)
        login(request, user)
        context = {
            "is_logged": request.user.is_authenticated
        }
        return HttpResponseRedirect('/home', context)
                    
"""
Add a review (login required).
This function handles the addition of a review. The user must be logged in to access this view.
Args:
    request (HttpRequest)
Returns:
    HttpResponse or HttpResponseRedirect: The response object.
"""
@login_required(login_url='/log_in')
def add_review(request):
    if request.method == 'GET':
        usuarios = User.objects.all()
        context = {
            "is_logged": request.user.is_authenticated,
            'current_page': 'add_review',
            'usuarios': usuarios,
        }
        return render(request,"app_inicial/add_review.html", context)
    if request.method =='POST':
        user_id = request.user
        #Contenido del documento
        title = request.POST['title']
        content = request.POST['content']
        request_to=request.POST['request_to']
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get("image")
        document = Document(
            creator=user_id, 
            title = title,
            request_to=request_to, 
            content=content,
            accepted=0,
            sign = None,
            )
        document.save()
        context = {
            'current_page': 'add_review',
        }
        return HttpResponseRedirect('/my_reviews', context)

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
        return render(request,"app_inicial/create_document.html")
    if request.method =='POST':
        user_id = request.user
        #Contenido del documento
        title = request.POST['title']
        content = request.POST['content']
        request_to=request.user
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get("image")
        cripticSign = sign(content.encode(), request.POST['secret_key'], "SHA-256")
        try:
            #Verifica que la Private Key entregada sea correcta para ese usuario
            verify(content.encode(), cripticSign, request.user.public_key)
        except:
            messages.error(request, 'La llave privada ingresada no es correcta.')
            return HttpResponseRedirect('/create_document')
        document = Document(
            creator=user_id, 
            title = title,
            request_to=request_to, 
            content=content,
            accepted=1,
            sign = cripticSign,
            )
        document.save()
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
def my_reviews(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    reviews = reviews.order_by('-date')
    mantainVotes(request, reviews)
    
    context = {
        "is_logged": request.user.is_authenticated, 
        "reviews": reviews,
        'current_page': 'my_reviews',
    }

    if request.method == 'POST':
        modify=request.POST['modify']
        if modify=='upvote':
            manageVote(request,1)
        if modify=='downvote':
            manageVote(request,-1)
        return HttpResponseRedirect('/my_reviews', context)

    return render(request, 'app_inicial/my_reviews.html', context)

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
Single review.
This function displays the information of a single review and allows users to comment on it.
Args:
    request (HttpRequest)
    id (int): The id of the review.
Returns:
    HttpResponse: The response object.
""" 
def single_review(request,id):
    context = {
        "is_logged": request.user.is_authenticated,
        'current_page': 'reviews',
    }
    if not id:
        return HttpResponseRedirect('/reviews', context)
    
    review=Review.objects.get(id=id)
    if not review:
        return HttpResponseRedirect('/reviews', context)

    comments = Comment.objects.filter(review_id=id)
    if request.user.is_authenticated:
        if Vote_Review.objects.filter(user_id=request.user, review_id=review).exists():
                review.isPositive=Vote_Review.objects.get(review=review,user=request.user).is_positive

    if request.method == 'GET': 
        context = {
            'is_logged': request.user.is_authenticated,
            'single_review':review, 
            'comments':comments,
            'current_page': 'reviews',
        }
        return render(request, 'app_inicial/single_review.html', context)
    
    if request.method == 'POST':
        modify=request.POST['modify']
        if modify=="delete":
            Review.objects.filter(id=id).delete()
            context = {
                "is_logged": request.user.is_authenticated,
                'current_page': 'reviews',
            }
            return HttpResponseRedirect('/reviews', context)
        
        elif modify=="edit":
            concert = request.POST['event']
            content = request.POST['content']
            stars = request.POST['puntuacion']
            review.content=content
            review.concert=concert
            review.stars=stars
            review.save()
        
        elif modify=="comment":
            if request.user.is_authenticated: 
                comment_content = request.POST['comment-content']
                if comment_content!="":    
                    current_datetime = datetime.datetime.now()
                    user_id = request.user
                    review_id = review
                    comment = Comment(
                        user_id=user_id,
                        review_id=review_id,
                        content=comment_content,
                        date=current_datetime
                        )
                    comment.save()
                    
        elif modify=="delete_comment":
            comment_id=request.POST['comment-id']
            comment=Comment.objects.get(id=comment_id)
            if comment.user_id==request.user:    
                comment.delete()
        
        elif modify=="edit_comment":
            comment_id=request.POST['comment-id']
            comment_content_edit= request.POST['comment-content-edit']
            comment=Comment.objects.get(id=comment_id)
            if comment.user_id==request.user:
                comment.content=comment_content_edit
                comment.save()
        
        elif modify=="upvote":
            manageVote(request,1)

        elif modify=="downvote":
            manageVote(request,-1)
        
        context = {
            'is_logged': request.user.is_authenticated,
            'single_review':review, 
            'comments':comments,
            'current_page': 'reviews',
        }

        return HttpResponseRedirect('/single_review/'+id, context)
