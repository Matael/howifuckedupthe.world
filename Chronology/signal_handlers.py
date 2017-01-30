from .utils import fill_with_wikipedia

def wikipedia_fill_handler(instance, raw, **kw):
    """
    Handler for Person.pre_save that fills the wiki_summary
    field with the data from wikipedia.

    This handler is called upon each save() and will fetch
    data from WP only if the field is empty.
    """

    if not raw and instance.wiki_summary=='':
        fill_with_wikipedia(instance)
