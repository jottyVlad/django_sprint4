from django.contrib import admin

from .models import Post, Category, Location, Comment


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    class Meta:
        model = Location


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category


admin.site.register(Comment)
