from django import template

register = template.Library()

@register.inclusion_tag('tags/timeline_event.html')
def timeline_event(event, n):
    return {
        'event': event,
        'n': n
    }
