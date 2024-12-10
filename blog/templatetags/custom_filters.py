from django import template

register = template.Library()

@register.filter(name='truncate_words')
def truncate_words(value, word_count):
    words = value.split()
    if len(words) > int(word_count):
        return ' '.join(words[:int(word_count)]) + '...'
    return value

@register.filter
def to(value, end):
    """
    Generates a range from the current value to the `end`.
    Usage: {% for i in 1|to:6 %}
    """
    return range(value, end + 1)


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value