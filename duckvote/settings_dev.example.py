# "I cannot use QuerySet or Manager with type annotations"
import django_stubs_ext
django_stubs_ext.monkeypatch()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$fzwp4^y4f8swcc$#j6+dtg2imt*zo8)^+28xeh)5^m#ty)#)i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# debug toolbar, also tailwind (for browser reload, presumably)
INTERNAL_IPS = [
    "127.0.0.1",
]

print("*** DEV ***")
