from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from almironmedia.utils.blocks import StoryBlock
from almironmedia.utils.models import BasePage


class ServicePage(BasePage):
    """A single service offered by the company."""

    template = "pages/service_page.html"
    parent_page_types = ["services.ServiceIndexPage"]
    subpage_types = []

    introduction = models.TextField(
        blank=True,
        help_text="Short summary. Shown at the top of the page and on the service cards.",
    )
    body = StreamField(StoryBlock(), blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        from almironmedia.forms.models import FormPage

        context = super().get_context(request, *args, **kwargs)
        # Target of the "Ask for a quote" button: the contact form in this language.
        context["contact_page"] = (
            FormPage.objects.live().public().filter(locale=self.locale).first()
        )
        return context


class ServiceIndexPage(BasePage):
    """Lists every published service underneath it, in the order set in the admin."""

    template = "pages/service_index_page.html"
    subpage_types = ["services.ServicePage"]
    max_count_per_parent = 1

    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock(), blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    def get_services(self):
        return ServicePage.objects.child_of(self).live().public().order_by("path")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["services"] = self.get_services()
        return context
