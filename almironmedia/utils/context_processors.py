from django.conf import settings
from django.utils.translation import get_language
from wagtail.models import Site


def global_vars(request):
    site = Site.find_for_request(request)
    return {
        "SEO_NOINDEX": settings.SEO_NOINDEX,
        "LANGUAGE_CODE": get_language() or settings.LANGUAGE_CODE,
        # Home page in the visitor's language, used by the header logo link.
        "home_page": site.root_page.localized if site else None,
    }
