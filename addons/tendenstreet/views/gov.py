import os

from tendenci.apps.theme.shortcuts import themed_response as render_to_resp

def cid(request, template_name="cid.html"):
    src = 'static/minutes/'
    minutes = os.listdir(src)
    context = {
        "page": {},     # Normal page info
        "minutes": [{
            'url': f'{src}/{filename}',
            'filename': filename
        } for filename in minutes]   # List of URLs
    }

    return render_to_resp(request=request, template_name=template_name,
            context=context)
