from django.contrib import admin
from .models import *

admin.site.register(PostModel)
admin.site.register(TagModel)
admin.site.register(CommentModel)
admin.site.register(NewsletterSubscriptionModel)
admin.site.register(LikeModel)

