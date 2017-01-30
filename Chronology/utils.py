import wikipedia


def fill_with_wikipedia(instance):
    """
    Check on wikipedia if a page matches
    the name and retrieve the summary if so.
    """

    wp_pages = wikipedia.search(instance.name)
    if len(wp_pages)>0:
        try:
            instance.wiki_summary = wikipedia.summary(wp_pages[0])
            instance.wiki_pagename = wp_pages[0]
        except wikipedia.DisambiguationError:
            pass

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
