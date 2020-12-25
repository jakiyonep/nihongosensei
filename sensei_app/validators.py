import os
from django.core.exceptions import ValidationError


def validate_pdf_or_MSO(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in ['.pdf', '.ppt','pptx', '.xlsx', '.doc', 'docx', 'xls']:
        raise ValidationError('アップロードできないファイルの種類です。')

def validate_file_size(value):
    filesize = value.size

    if filesize > 10485760:
        raise ValidationError("10MBを超えるファイルはアップロードできません。")
    else:
        return value