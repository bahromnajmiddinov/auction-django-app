from django.core.exceptions import ValidationError

import os


def validate_video_file_extension(value):
    ext = os.path.splittext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid Video File Extension')

