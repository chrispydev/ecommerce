""" module imports"""
from django.contrib import admin
# from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("", include("store.urls")),
    path("api/", include("store.api_urls")),
    path("account/", include("customer.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# urlpatterns += i18n_patterns(
#     path('i18n/', include('django.conf.urls.i18n')),
# )

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if not settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)