from django.contrib import admin
from models import Image, News
from django.utils.translation import ugettext as _

class ChoiceInline(admin.StackedInline):
    model = Image
    fieldsets = [ ( None, {'fields': ['image_url', 'image', 'title', 'alt']}),
                ]
    extra = 3


class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
                  ( _('news details'),      {'fields': ['author', 'title', 'text', 'is_published', 'news_language']}),
                  ( _('date information'), {'fields': ['pubblication_date']}),
                ]

    inlines = [ChoiceInline]
    list_display = ('title', 'author', 'modified_by', 'pubblication_date', 'news_language', 'is_published')
    list_editable = ('is_published',)
    list_filter = ['pubblication_date', 'is_published', 'news_language']
    search_fields = ['title']
    date_hierarchy = 'pubblication_date'
    

    def queryset(self, request):
        """
            Reset default object manager for admin view
        """
        return News.objects.all()
    

    def add_view(self, request, form_url='', extra_context=None):
        self._created_by_user = request.user
        return super(NewsAdmin, self).add_view(request, form_url, extra_context)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author" and hasattr(self, '_created_by_user'):
            kwargs["initial"] = self._created_by_user.pk
    
        return super(NewsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        obj.save()


admin.site.register(News, NewsAdmin)
