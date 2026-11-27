from django import template


register = template.Library()


@register.filter
def fa_digits(value):
    if value is None:
        return value

    english_digits = '0123456789'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'

    translation = str.maketrans(english_digits, persian_digits)
    return str(value).translate(translation)

@register.filter
def jalali_date(value):
    if value is None:
        return ''

    import jdatetime

    jalali = jdatetime.date.fromgregorian(date=value)
    return jalali.strftime('%Y/%m/%d')