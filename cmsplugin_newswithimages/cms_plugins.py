from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import NewsPlugin, News
from django.utils.translation import ugettext as _


class CMSNewsWithImagePlugin(CMSPluginBase):
    model = NewsPlugin
    name = _("News manager")
    render_template = "cmsplugin_newswithimages/news.html"

    def render(self, context, instance, placeholder):

        if instance.news_language == 'all':
            latest_news = News.publisher.all()[:instance.max_news]
        else:
            latest_news = News.publisher.all().filter(news_language=instance.news_language)[:instance.max_news]

        context.update({
            'header':_("news"),
            'information': latest_news 
        })
        return context

plugin_pool.register_plugin(CMSNewsWithImagePlugin)
