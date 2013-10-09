from django.conf.urls import patterns, url

from voice_uploads import views

urlpatterns = patterns('',
    # our root
    url(r'^$', views.index, name='index'),

    # authorising callback from soundcloud
    url(r'^auth/$', views.auth, name='auth'),

    # show the upload button
    url(r'start$', views.start, name="start"),

    # the ajax file handler
    url(r'ajax-upload$', views.import_uploader, name="my_ajax_upload"),

    # handle the uploaded file, send it to SC
    url(r'^upload/$', views.upload, name='upload'),
)