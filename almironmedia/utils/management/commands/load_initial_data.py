"""
Create the starter content for the Almiron Media site: home page, services
and contact form, in Catalan (default language) and Spanish.

The texts are a starting point meant to be edited from the Wagtail admin.
The command does nothing if the site already has pages below the home page.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.test.utils import override_settings
from wagtail.models import Locale, Page, Site

from almironmedia.forms.models import FormField, FormPage
from almironmedia.home.models import HomePage
from almironmedia.navigation.models import NavigationSettings
from almironmedia.services.models import ServiceIndexPage, ServicePage


def section(heading, *paragraphs):
    return {
        "type": "section",
        "value": {
            "heading": heading,
            "content": [{"type": "paragraph", "value": html} for html in paragraphs],
        },
    }


def bullets(*items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


HOME = {
    "ca": {
        "title": "Almiron Media",
        "introduction": (
            "Consultoria informàtica independent al Vallès Oriental. "
            "Ajudem autònoms i petites empreses a tenir una informàtica que funciona, "
            "és segura i els fa la feina més fàcil."
        ),
        "cta_title": "Tens un projecte o un problema informàtic?",
        "cta_text": "<p>Explica'ns què necessites i et respondrem amb una proposta clara.</p>",
        "cta_button": "Contacta'ns",
    },
    "es": {
        "title": "Almiron Media",
        "slug": "inicio",
        "introduction": (
            "Consultoría informática independiente en el Vallès Oriental. "
            "Ayudamos a autónomos y pequeñas empresas a tener una informática que funciona, "
            "es segura y les hace el trabajo más fácil."
        ),
        "cta_title": "¿Tienes un proyecto o un problema informático?",
        "cta_text": "<p>Cuéntanos qué necesitas y te responderemos con una propuesta clara.</p>",
        "cta_button": "Contáctanos",
    },
}

SERVICES_INDEX = {
    "ca": {
        "title": "Serveis",
        "slug": "serveis",
        "introduction": "Tot el que la teva empresa necessita en informàtica, amb un sol interlocutor.",
    },
    "es": {
        "title": "Servicios",
        "slug": "servicios",
        "introduction": "Todo lo que tu empresa necesita en informática, con un único interlocutor.",
    },
}

SERVICES = [
    {
        "ca": {
            "title": "Consultoria informàtica",
            "slug": "consultoria-informatica",
            "introduction": (
                "Analitzem com treballes i et proposem les eines i la infraestructura "
                "que encaixen amb el teu negoci i el teu pressupost."
            ),
            "heading": "Què inclou",
            "items": [
                "Auditoria dels equips, la xarxa i el programari actuals",
                "Pla de millora amb prioritats i costos",
                "Acompanyament en la compra i la posada en marxa",
            ],
        },
        "es": {
            "title": "Consultoría informática",
            "slug": "consultoria-informatica",
            "introduction": (
                "Analizamos cómo trabajas y te proponemos las herramientas y la infraestructura "
                "que encajan con tu negocio y tu presupuesto."
            ),
            "heading": "Qué incluye",
            "items": [
                "Auditoría de los equipos, la red y el software actuales",
                "Plan de mejora con prioridades y costes",
                "Acompañamiento en la compra y la puesta en marcha",
            ],
        },
    },
    {
        "ca": {
            "title": "Ciberseguretat",
            "slug": "ciberseguretat",
            "introduction": (
                "Revisem la seguretat dels teus sistemes i t'ajudem a protegir les dades "
                "de l'empresa i dels teus clients."
            ),
            "heading": "Què inclou",
            "items": [
                "Revisió de seguretat i proves d'intrusió",
                "Còpies de seguretat i pla de recuperació",
                "Formació pràctica per a l'equip",
            ],
        },
        "es": {
            "title": "Ciberseguridad",
            "slug": "ciberseguridad",
            "introduction": (
                "Revisamos la seguridad de tus sistemas y te ayudamos a proteger los datos "
                "de la empresa y de tus clientes."
            ),
            "heading": "Qué incluye",
            "items": [
                "Revisión de seguridad y pruebas de intrusión",
                "Copias de seguridad y plan de recuperación",
                "Formación práctica para el equipo",
            ],
        },
    },
    {
        "ca": {
            "title": "Desenvolupament web i aplicacions",
            "slug": "desenvolupament-web",
            "introduction": (
                "Webs i aplicacions a mida, fàcils de gestionar i pensades perquè "
                "les puguis actualitzar tu mateix."
            ),
            "heading": "Què inclou",
            "items": [
                "Webs corporatives amb gestor de continguts",
                "Aplicacions internes i automatització de tasques",
                "Allotjament, domini i manteniment",
            ],
        },
        "es": {
            "title": "Desarrollo web y aplicaciones",
            "slug": "desarrollo-web",
            "introduction": (
                "Webs y aplicaciones a medida, fáciles de gestionar y pensadas para que "
                "puedas actualizarlas tú mismo."
            ),
            "heading": "Qué incluye",
            "items": [
                "Webs corporativas con gestor de contenidos",
                "Aplicaciones internas y automatización de tareas",
                "Alojamiento, dominio y mantenimiento",
            ],
        },
    },
    {
        "ca": {
            "title": "Suport i manteniment",
            "slug": "suport-i-manteniment",
            "introduction": (
                "Assistència quan alguna cosa falla i manteniment preventiu perquè "
                "falli el mínim possible."
            ),
            "heading": "Què inclou",
            "items": [
                "Suport remot i presencial",
                "Manteniment d'ordinadors, xarxes i servidors",
                "Instal·lació i configuració d'equips nous",
            ],
        },
        "es": {
            "title": "Soporte y mantenimiento",
            "slug": "soporte-y-mantenimiento",
            "introduction": (
                "Asistencia cuando algo falla y mantenimiento preventivo para que "
                "falle lo menos posible."
            ),
            "heading": "Qué incluye",
            "items": [
                "Soporte remoto y presencial",
                "Mantenimiento de ordenadores, redes y servidores",
                "Instalación y configuración de equipos nuevos",
            ],
        },
    },
]

CONTACT = {
    "ca": {
        "title": "Contacte",
        "slug": "contacte",
        "introduction": "<p>Explica'ns què necessites i et respondrem tan aviat com puguem.</p>",
        "action_text": "Envia",
        "thank_you_text": "<p>Gràcies! Hem rebut el teu missatge i et respondrem ben aviat.</p>",
        "subject": "Nou missatge des del web",
        "fields": ["Nom", "Correu electrònic", "Telèfon", "Missatge"],
    },
    "es": {
        "title": "Contacto",
        "slug": "contacto",
        "introduction": "<p>Cuéntanos qué necesitas y te responderemos lo antes posible.</p>",
        "action_text": "Enviar",
        "thank_you_text": "<p>¡Gracias! Hemos recibido tu mensaje y te responderemos muy pronto.</p>",
        "subject": "Nuevo mensaje desde la web",
        "fields": ["Nombre", "Correo electrónico", "Teléfono", "Mensaje"],
    },
}

# (field type, required) for each contact form field, in order.
CONTACT_FIELD_TYPES = [
    ("singleline", True),
    ("email", True),
    ("singleline", False),
    ("multiline", True),
]


def service_fields(data):
    return {
        "title": data["title"],
        "slug": data["slug"],
        "introduction": data["introduction"],
        "body": [section(data["heading"], bullets(*data["items"]))],
    }


def home_body(data, contact_page):
    return [
        {
            "type": "cta",
            "value": {
                "title": data["cta_title"],
                "text": data["cta_text"],
                "button": [
                    {
                        "type": "internal",
                        "value": {"page": contact_page.pk, "title": data["cta_button"]},
                    }
                ],
            },
        }
    ]


def translate(page, locale, **fields):
    """Create and publish the translation of `page` with the given field values."""
    translation = page.copy_for_translation(locale)
    for name, value in fields.items():
        setattr(translation, name, value)
    translation.save_revision().publish()
    return translation


class Command(BaseCommand):
    help = "Create the starter pages (home, services, contact) in Catalan and Spanish"

    # Translations start as copies and are then renamed; that is not a URL
    # change visitors could have bookmarked, so no redirects are needed.
    @override_settings(WAGTAILREDIRECTS_AUTO_CREATE=False)
    @transaction.atomic
    def handle(self, **options):
        # A fresh install only has the empty home page created by the migrations.
        if Page.objects.filter(depth__gt=2).exists():
            self.stdout.write("The site already has content; nothing to do.")
            return

        catalan = Locale.get_default()
        spanish, _ = Locale.objects.get_or_create(language_code="es")

        # Replace the placeholder page Wagtail creates on install.
        Page.objects.filter(depth=2).delete()
        root = Page.get_first_root_node()
        root = Page.objects.get(pk=root.pk)

        home = HomePage(
            title=HOME["ca"]["title"],
            slug="home",
            introduction=HOME["ca"]["introduction"],
            locale=catalan,
            # The body needs the contact page, which does not exist yet.
            body=[section("Almiron Media", "<p></p>")],
        )
        root.add_child(instance=home)

        Site.objects.all().delete()
        site = Site.objects.create(
            hostname="localhost",
            port=80,
            root_page=home,
            site_name="Almiron Media",
            is_default_site=True,
        )

        index_data = SERVICES_INDEX["ca"]
        services_index = ServiceIndexPage(locale=catalan, **index_data)
        home.add_child(instance=services_index)

        services = []
        for service in SERVICES:
            page = ServicePage(locale=catalan, **service_fields(service["ca"]))
            services_index.add_child(instance=page)
            services.append(page)

        contact_data = CONTACT["ca"]
        contact = FormPage(
            locale=catalan,
            **{k: v for k, v in contact_data.items() if k != "fields"},
        )
        home.add_child(instance=contact)
        for order, (label, (field_type, required)) in enumerate(
            zip(contact_data["fields"], CONTACT_FIELD_TYPES)
        ):
            FormField.objects.create(
                page=contact,
                sort_order=order,
                label=label,
                field_type=field_type,
                required=required,
            )

        home.body = home_body(HOME["ca"], contact)
        home.save_revision().publish()

        # Spanish translations
        translate(
            home,
            spanish,
            slug=HOME["es"]["slug"],
            introduction=HOME["es"]["introduction"],
            body=home_body(HOME["es"], contact),
        )
        translate(services_index, spanish, **SERVICES_INDEX["es"])
        for page, service in zip(services, SERVICES):
            translate(page, spanish, **service_fields(service["es"]))

        contact_es_data = CONTACT["es"]
        contact_es = translate(
            contact,
            spanish,
            **{k: v for k, v in contact_es_data.items() if k != "fields"},
        )
        for field, label in zip(
            contact_es.form_fields.order_by("sort_order"), contact_es_data["fields"]
        ):
            field.label = label
            field.save()

        # Main menu. Links follow the visitor's language automatically.
        navigation = NavigationSettings.for_site(site)
        navigation.primary_navigation = [
            {"type": "link", "value": {"page": services_index.pk, "title": ""}},
            {"type": "link", "value": {"page": contact.pk, "title": ""}},
        ]
        navigation.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {Page.objects.filter(depth__gt=1).count()} pages "
                "in Catalan (/) and Spanish (/es/)."
            )
        )
