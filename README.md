# almironmedia-web

Web de Almiron Media (servicios informáticos), hecha con [Wagtail](https://wagtail.org)
a partir de la plantilla [wagtail/news-template](https://github.com/wagtail/news-template).

- **Idiomas:** catalán (por defecto, en `/`) y castellano (en `/es/`).
- **Secciones:** portada, servicios y contacto con formulario.
- El blog de noticias de la plantilla sigue en el código (`almironmedia/news`) pero no
  tiene páginas ni enlaces; se puede activar creando una página de noticias desde el panel.

## Puesta en marcha

Necesitas Python 3.12 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
python bootstrap.py              # instala dependencias, crea la base de datos y las páginas iniciales
python manage.py createsuperuser # tu usuario para el panel
python manage.py runserver
```

- Web: http://localhost:8000
- Panel de edición: http://localhost:8000/admin/

`python bootstrap.py --no-sample-data` hace lo mismo sin crear las páginas iniciales.

## Cómo está organizado

| Qué | Dónde |
| --- | --- |
| Páginas de servicios (índice y servicio) | `almironmedia/services/` |
| Portada | `almironmedia/home/` |
| Formulario de contacto | `almironmedia/forms/` |
| Textos iniciales en catalán y castellano | `almironmedia/utils/management/commands/load_initial_data.py` |
| Plantillas HTML | `templates/` |
| Textos fijos de la interfaz (buscar, enviar…) | `locale/ca` y `locale/es` |
| Estilos (Tailwind + Sass) | `static_src/`, compilados en `static_compiled/` |

### Editar contenido

Todo el contenido se edita desde el panel. Cada página tiene su versión en el otro idioma:
en el menú «…» de la página, **Traducir**. El menú principal se configura en
*Ajustes → Navigation settings* y enlaza solo a la versión del idioma del visitante.

Los mensajes del formulario de contacto se guardan en el panel (*Formularios*). Para
recibirlos también por correo, rellena «Dirección de destino» en la página de contacto y
configura el envío de correo (`EMAIL_*`) en producción.

### Cambiar estilos

```bash
npm ci
npm run build:prod   # o `npm start` para recompilar al guardar
```

### Cambiar textos fijos de la interfaz

Edita `locale/<idioma>/LC_MESSAGES/django.po` y recompila con `python manage.py compilemessages`
(requiere gettext) o, sin gettext:

```bash
pip install polib
python -c "import polib; [polib.pofile(f'locale/{l}/LC_MESSAGES/django.po').save_as_mofile(f'locale/{l}/LC_MESSAGES/django.mo') for l in ('ca','es')]"
```

## Tests

```bash
python manage.py test
```

## Publicación

En producción usa `DJANGO_SETTINGS_MODULE=almironmedia.settings.production` y define al menos
`SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y `DATABASE_URL`. El repositorio incluye
el `Dockerfile` y el `fly.toml` de la plantilla como punto de partida.
