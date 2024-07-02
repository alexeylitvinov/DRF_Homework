from rest_framework.exceptions import ValidationError


class ValidateLink:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is None:
            value[self.field] = None
            return
        if (not tmp_val.startswith('https://www.youtube.com/')
            and not tmp_val.startswith('https://youtu.be/')) \
                and not tmp_val.startswith('https://www.youtube.com/'):
            raise ValidationError('Ожидается ссылка на YouTube')
