from django.http import HttpResponse
from django.template import loader
import json
import os

# reaching tools demands the path adjustments
import sys
sys.path.append('..')
sys.path.append('..')
import tools


def index(request):
    track_file = open(os.path.join(tools.PROGRAM_MAIN_DIR, 'track_results.json'))
    track_file_content = json.loads(track_file.read())
    track_file.close()
    print tools.PROGRAM_MAIN_DIR
    print os.path.join(tools.PROGRAM_MAIN_DIR, 'track_site\\templates\\track_site\\index.html')
    template = loader.get_template(os.path.join(tools.PROGRAM_MAIN_DIR,
                                                'track_site\\templates\\track_site\\index.html'))
    context = {
        'results': track_file_content,
    }
    return HttpResponse(template.render(context, request))


def graph(request):
    track_file = open(os.path.join(tools.PROGRAM_MAIN_DIR, 'track_results.json'))
    content = json.loads(track_file.read())
    dates = [i for i in range(len(content))]
    corrects = [float(record["CORRECT"]) for record in content]
    template = loader.get_template(os.path.join(tools.PROGRAM_MAIN_DIR,
                                                'track_site\\templates\\track_site\\graph.html'))
    context = {
        'dates': dates,
        'corrects': corrects,
    }
    return HttpResponse(template.render(request=request, context=context))


def js(request):
    js_file = open(os.path.join(tools.PROGRAM_MAIN_DIR, 'track_site\\templates\\track_site\\Chart.js'))
    return HttpResponse(js_file.read())
