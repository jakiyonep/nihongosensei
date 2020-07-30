

@register.filter
def markdownify(text):
    # safe mode is deprecated, see: https://pythonhosted.org/Markdown/reference.html#safe_mode
    untrusted_text = markdown.markdown(text, safe_mode='escape')
    html = bleach.clean(untrusted_text,
                        tags=settings.MARKDOWNIFY_WHITELIST_TAGS,
			attributes=settings.MARKDOWNIFY_WHITELIST_ATTRS, ) # Add this line
    html = bleach.linkify(html)
    return html