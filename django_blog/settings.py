"""
Django settings for django_blog project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-nyyo&i48=9h4lue^+d4v_i&gbe906#@ho3n$(uf9(2veh2i(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 这个参数的设置是为了限制一些主机的访问的,当DEBUG=False的时候,这个值是必须要设定的,否则,启动会报错,其值是一个列表,可以是ip地址,也可以是域名还可以支持通配符,如['example.com','192.168.1.2',‘*.example.com’],如果不想有人访问不了可以直接使用['*'],所有都可以访问
# https://blog.csdn.net/heatdeath/article/details/71076333
ALLOWED_HOSTS = ['*']

# Application definition,需要注意最后一个模块也需要加 逗号 否则部署可能会出现最后一个模块找不到的情况

INSTALLED_APPS = [
    'django.contrib.admin',  # 管理站点
    'django.contrib.auth',  # 用户认证系统
    'django.contrib.contenttypes',  # 用于内容类型的框架
    'django.contrib.sessions',  # 会话框架
    'django.contrib.messages',  # 消息框架
    # 加入配置在Template模版文件中可以设置{{ STATIC_URL }} 作为静态资源文件路径前缀,另一项配置在TEMPLATES中
    'django.contrib.staticfiles',
    'common',
    'user',
    'blog',
    'remote'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', #注释该行避免表单请求403错误,否则每个表单下都需要添加出csrf表达式
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates").replace('\\', '/'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 加入配置在Template模版文件中可以设置{{ STATIC_URL }} 作为静态资源文件路径前缀,另一项配置在INSTALLED_APPS中
                'django.template.context_processors.static',

            ],
        },

    },
]

WSGI_APPLICATION = 'django_blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'mysql',  Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle',
        # 'USER': 'root',  # Not used with sqlite3.
        # 'PASSWORD': '123456', # Not used with sqlite3.
        # 'HOST': 'localhost',  # Not used with sqlite3.
        # 'PORT': '3306', # Not used with sqlite3.
    }
}

# 配置打印sql
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# 配置Django缓存(缓存)：
'''
Django默认支持Session，其内部提供了5种类型的Session供开发者使用(使用方法一样,配置略有差别)：
数据库（默认）即：django_session 表中。
缓存
文件
缓存+数据库
加密cookie
'''
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
SESSION_CACHE_ALIAS = 'default'  # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# admin管理界面改成中文zh-Hant是繁体中文zh-Hans是简体中文
LANGUAGE_CODE = 'zh-Hans'

# 有两个配置参数是跟时间与时区有关的，分别是TIME_ZONE和USE_TZ
# 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
# 如果USE_TZ 设置为False，而TIME_ZONE设置为None，则Django还是会使用默认的America/Chicago时间。
# 若TIME_ZONE设置为其它时区的话，则还要分情况，如果是Windows系统，则TIME_ZONE设置是没用的，Django会使用本机的时间。
# 如果为其他系统，则使用该时区的时间，入设置USE_TZ = False, TIME_ZONE = 'Asia/Shanghai', 则使用上海的UTC时间。
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_URL = '/user/login'

# 一般用来设置通用的静态资源，对应的目录不放在APP下，而是放在Project下
STATICFILES_DIRS = (
    (os.path.join(BASE_DIR, 'static/')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# 项目部署时需要配置该项 代码上传到服务器后需要先运行命令 python manage.py collectstatic 此时就可以将项目中【它会把app下的static目录，
# 项目根目录下的static目录，还有STATICFILES_DIRS下的静态文件保存起来】收集到STATIC_ROOT中,使用 join做组合路径时,后面的路径不要加 / 否则路径为根目录
# https://blog.csdn.net/jj546630576/article/details/78606531
STATIC_ROOT = os.path.join(BASE_DIR, 'web')

# 用户上传后的文件,在项目中保存的路径，经常由FileFields字段上传
MEDIA_ROOT = ''

# 通过URL来访问这个本地地址的URL
# https://blog.csdn.net/geerniya/article/details/78958243
MEDIA_URL = ''
