from django import template

register = template.Library()

@register.filter(name='replace_fields')
def replace_fields(value, fields):
    """Заменяет {field} на [field] для предпросмотра"""
    if not value or not fields:
        return value
    
    for field in fields:
        value = value.replace(f'{{{field}}}', f'[{field}]')
    return value