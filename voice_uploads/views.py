from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template import RequestContext, loader

from django.middleware.csrf import get_token
from django.shortcuts import render_to_response

from ajaxuploader.views import AjaxFileUploader

import soundcloud

CLIENT_ID     = 'via email'
CLIENT_SECRET = 'via email'
REDIRECT_URL  = 'http://gloobook.co.za:8000/soundcloud/voice/auth/' # Needs to correspond to the SoundCloud app settings

GROUP_ID      = 126877 # Jacaranda
# GROUP_ID    = 133436 # East Coast


# The index page - just force a redirect for now
def index(request):

    # Create SC object with app credentials
    client    = soundcloud.Client( client_id     = CLIENT_ID    ,
                                   client_secret = CLIENT_SECRET,
                                   redirect_uri  = REDIRECT_URL   )

    # Redirect to SC authorize URL
    return HttpResponseRedirect(client.authorize_url())



def auth(request):
    
    # Create SC object with app credentials
    client    = soundcloud.Client( client_id     = CLIENT_ID    ,
                                   client_secret = CLIENT_SECRET,
                                   redirect_uri  = REDIRECT_URL   )

    # Exchange authorization code for access token
    code         = request.GET.get('code', '')
    access_token = client.exchange_token(code)

    # We should actually save this access token in the db - connected to the user.
    # i.e.: Not just a session var
    request.session['access_token'] = access_token.access_token

    # make an authenticated call
    client       = soundcloud.Client(access_token = request.session['access_token'])
    user         = client.get('/me')


    # Here we can do _things_ to the user  ;)



    return HttpResponseRedirect('../start')


def start(request):
    csrf_token = get_token(request)
    return render_to_response(
                'import.html',
                {
                    'csrf_token': csrf_token,
                    'root_url': '/soundcloud/voice'
                },
                context_instance = RequestContext(request)
    )



import_uploader = AjaxFileUploader()



def upload(request):

    # Absolute path to the file.
    track = "C:/xampp/htdocs/soundcloud/jacaranda/uploads/" + request.GET.get('filename', '')

    # Use the access token instead of going through the whole process
    client       = soundcloud.Client(access_token = request.session['access_token'])

    # Upload audio file to SC
    upload       = client.post('/tracks', track={
        'title': 'This is an uploaded sound',
        'asset_data': open(track, 'rb')
    })

    # Contribute track to the group
    group        = client.post('/groups/%d/contributions' % (GROUP_ID,), track={
        'id': upload.id
    })

    # Our page template
    template     = loader.get_template('index.html')

    # Set the variables we'll use in the page
    context      = RequestContext(request, {
        'title': upload.title
    })

    return HttpResponse(template.render(context))