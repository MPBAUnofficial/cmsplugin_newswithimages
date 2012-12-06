from django.db import models
from django.conf import settings
from cms.models import CMSPlugin
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


import django.utils.timezone as timezone


class NewsPublisherManager(models.Manager):
    def get_query_set(self):
        return super(NewsPublisherManager, self).get_query_set() \
                .filter(pubblication_date__lte=timezone.now()) \
                .filter(is_published=True) \
                .order_by('pubblication_date')


class News(models.Model):

    author = models.ForeignKey(
                                User, 
                                null=True, 
                                on_delete=models.SET_NULL, 
                                verbose_name=_("author"), 
                                related_name="user_author_set"
                              )

    modified_by = models.ForeignKey(
                               User,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_("modified by"),
                               related_name="user_modifier_set"
                               )

    title = models.CharField(
                              _("title"),
                              max_length=20,
                              help_text=_("the title of the news"),
                            ) 

    pubblication_date = models.DateTimeField \
                 (
                   _("pubblication date"),
                   default= timezone.now(),
                   help_text=_("the date in which the news will be published"),
                 )

    is_published = models.BooleanField \
                       (
                         _('published'), 
                         default=True,
                         help_text=_("decide if the news is published or not"),
                       )
    
    text = models.TextField(
                             _("text"),
                             help_text=_("the text of the news"),
                           )
    
    news_language = models.CharField \
                    ( 
                      verbose_name=_("language"),
                      choices = [(code,description) \
                                for (code,description) in settings.LANGUAGES],
                      max_length=20,
                    )

    publisher = NewsPublisherManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title or str(self.pk)

    class Meta:
        verbose_name=_("news")
        verbose_name_plural=_("news")
        ordering = ['pubblication_date']



class Image(models.Model):
    
    news = models.ForeignKey(News)
    
    image_url = models.URLField \
        (
           _("alternative image url"),
           verify_exists=True,
           null=True,
           blank=True,
           help_text=_("this URL is used only if no image are specified")
         )
    
    image = FilerImageField(
                              null=True,
                              blank=True,
                              verbose_name=_("image"),
                              related_name="image_source_set", 
                           )
        
    title = models.CharField(
                               _("title"),
                               max_length=255,
                               blank=True
                            )
    
    alt = models.CharField(
                             _("alt text"),
                             max_length=80,
                             blank=True
                          )
    def clean(self):
        if not self.image and not self.image_url:
            raise ValidationError(_("Image not specified, use image or alternative url to specify the image source"))

    def __unicode__(self):
        return self.title or self.alt or str(self.pk)

    class Meta:
        verbose_name=_("image")
        verbose_name_plural=_("images")


class NewsPlugin(CMSPlugin):
    max_news = models.PositiveIntegerField \
                                    (
                                      verbose_name= _("limit of news"),
                                      help_text = _("how many news to diplay"),
                                      default = 3,
                                    )

    news_language = models.CharField \
                ( 
                  verbose_name=_("language"),
                  choices = [(code,description) for (code,description) in \
                                     settings.LANGUAGES] + [('all', _('All'))],
                  default = 'all',
                  max_length=20,
                )

    def __unicode__(self):
        return _(u'showing %(count)d news') % {'count': self.max_news}
