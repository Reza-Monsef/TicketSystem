from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 1002400:
        raise ValidationError(
            "فایل نباید بیشتر از ۱ مگابایت حجم داشته باشد")
    else:
        return value
