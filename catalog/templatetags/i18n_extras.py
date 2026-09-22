from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Arabic has no single national flag — it's the official language of 20+
# countries. The closest thing to a shared "Arab" flag is the Pan-Arab
# colours (black / white / green bands + red hoist triangle), the palette
# nearly every modern Arab state's flag was later derived from, so that's
# what's used here instead of picking one country arbitrarily.
_PAN_ARAB_FLAG_SVG = mark_safe(
    '<svg viewBox="0 0 24 16" class="inline-block h-4 w-6 rounded-[2px] align-middle" '
    'role="img" aria-label="Pan-Arab bayrağı">'
    '<rect width="24" height="16" fill="#fff"/>'
    '<rect width="24" height="5.33" fill="#000"/>'
    '<rect y="10.67" width="24" height="5.33" fill="#007A3D"/>'
    '<polygon points="0,0 9,8 0,16" fill="#CE1126"/>'
    "</svg>"
)

_FLAGS = {
    "tr": "🇹🇷",
    "en": "🇬🇧",
    "fr": "🇫🇷",
    "es": "🇪🇸",
    "ar": _PAN_ARAB_FLAG_SVG,
}


@register.filter
def flag_for(language_code):
    return _FLAGS.get(language_code, "")
