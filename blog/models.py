from django.db import models
from django.utils.text import slugify
from authentication.models import UserModel


class TagModel(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = "Tags"


class PostModel(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    tag = models.ForeignKey(TagModel, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='post_images/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='liked_from')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='liked_to')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.post}'

    class Meta:
        db_table = 'like'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class NewsletterSubscriptionModel(models.Model):
    email = models.EmailField(unique=True)

    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'blog_newsletter_subscription'
        verbose_name = 'NewsletterSubscription'
        verbose_name_plural = 'NewsletterSubscriptions'
