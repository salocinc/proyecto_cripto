from django.contrib import admin
from app_inicial.models import User
from app_inicial.models import Review
from app_inicial.models import Comment
from app_inicial.models import Location
from app_inicial.models import Vote_Review
from app_inicial.models import Document



# Register your models here.
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Location)
admin.site.register(Vote_Review)
admin.site.register(Document)


