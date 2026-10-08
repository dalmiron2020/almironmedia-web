from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index

from wagtail.fields import StreamField
from almironmedia.utils.blocks import StoryBlock, InternalLinkBlock
from almironmedia.utils.models import BasePage


class HomePage(BasePage):
    template = "pages/home_page.html"
    introduction = models.TextField(blank=True)
    hero_cta = StreamField(
        [("link", InternalLinkBlock())],
        blank=True,
        min_num=0,
        max_num=1,
    )
    body = StreamField(StoryBlock())
    featured_section_title = models.TextField(blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("hero_cta"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("featured_section_title", heading="Title"),
                InlinePanel(
                    "page_related_pages",
                    label="Pages",
                    max_num=12,
                ),
            ],
            heading="Featured section",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        # Imported here to keep the home app importable on its own.
        from almironmedia.services.models import ServiceIndexPage, ServicePage

        context = super().get_context(request, *args, **kwargs)
        context["services_index"] = (
            ServiceIndexPage.objects.live().public().filter(locale=self.locale).first()
        )
        context["services"] = (
            ServicePage.objects.live()
            .public()
            .filter(locale=self.locale)
            .order_by("path")
        )
        return context
