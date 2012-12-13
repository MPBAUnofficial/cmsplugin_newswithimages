from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import NewsPlugin, News
from django.utils.translation import ugettext as _


class CMSNewsWithImagePlugin(CMSPluginBase):
    model = NewsPlugin
    name = _("News manager")
    render_template = "cmsplugin_newswithimages/rotating-news.html"

    def render(self, context, instance, placeholder):

        if instance.news_language == 'all':
            all_news = News.publisher.all()
        else:
            all_news = News.publisher.all().filter(news_language=instance.news_language)

        if instance.rotate_element == False:
            latest_news = all_news[:instance.max_news]
            rotate_news = False
        else:
            latest_news = all_news

            if (len(all_news) > instance.max_news):
                rotate_news = instance.rotate_element
            else:
                rotate_news = False

        if rotate_news == False:
            self.render_template = "cmsplugin_newswithimages/news.html"

        context.update({
            'header':_("news"),
            'information': latest_news, 
            'visible_news': instance.max_news,
            'id':instance.id,
        })
        return context

plugin_pool.register_plugin(CMSNewsWithImagePlugin)
