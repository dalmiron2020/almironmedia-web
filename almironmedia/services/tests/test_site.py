from django.core.management import call_command
from django.test import TestCase
from wagtail.contrib.forms.models import FormSubmission

from almironmedia.services.models import ServicePage


class StarterSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_initial_data", verbosity=0)

    def test_pages_render_in_both_languages(self):
        for url in [
            "/",
            "/serveis/",
            "/serveis/ciberseguretat/",
            "/contacte/",
            "/es/",
            "/es/servicios/",
            "/es/servicios/ciberseguridad/",
            "/es/contacto/",
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_home_lists_services_in_the_page_language(self):
        response = self.client.get("/es/")
        self.assertContains(response, "Ciberseguridad")
        self.assertNotContains(response, "Ciberseguretat")
        self.assertContains(response, 'lang="es"')

    def test_menu_links_follow_the_language(self):
        self.assertContains(self.client.get("/"), 'href="/serveis/"')
        self.assertContains(self.client.get("/es/"), 'href="/es/servicios/"')

    def test_every_service_is_translated(self):
        for service in ServicePage.objects.filter(locale__language_code="ca"):
            self.assertTrue(service.get_translations().live().exists())

    def test_contact_form_stores_the_message(self):
        response = self.client.post(
            "/es/contacto/",
            {
                "nom": "Prueba",
                "correu_electronic": "prueba@example.com",
                "telefon": "",
                "missatge": "Hola",
            },
        )
        self.assertContains(response, "Hemos recibido tu mensaje")
        self.assertEqual(FormSubmission.objects.count(), 1)

    def test_running_the_command_twice_changes_nothing(self):
        before = ServicePage.objects.count()
        call_command("load_initial_data", verbosity=0)
        self.assertEqual(ServicePage.objects.count(), before)
