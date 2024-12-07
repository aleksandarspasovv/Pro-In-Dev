from django import template

register = template.Library()

@register.filter
def extract_username(url):
    if url and "/" in url:
        return url.rstrip('/').split('/')[-1]
    return url
