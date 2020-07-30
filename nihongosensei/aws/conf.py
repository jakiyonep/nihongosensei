import os

DEFAULT_FILE_STORAGE = 'nihongosensei.aws.utils.MediaRootS3BotoStorage'
# <project-name> = Django プロジェクト名
STATICFILES_STORAGE = 'nihongosensei.aws.utils.StaticRootS3BotoStorage'
# <project-name> = Django プロジェクト名

AWS_ACCESS_KEY_ID = os.environ.get('NIHONGOSENSEI_ACCESS_KEY_ID')  # 環境変数を指定
AWS_SECRET_ACCESS_KEY = os.environ.get('NIHONGOSENSEI_SECRET_ACCESS_KEY')  # 環境変数を指定

AWS_STORAGE_BUCKET_NAME = 'nihongosensei'  # Amazon S3 のバケット名
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # キャッシュの有効期限（最長期間）= 1日
}
AWS_QUERYSTRING_AUTH = False  # URLからクエリパラメータを削除

AWS_S3_URL = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_URL, 'media')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_URL, 'static')