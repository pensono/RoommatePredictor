import json

from django.http import HttpResponse
from django.template import loader

from . import predictor


def index(request):
    template = loader.get_template('index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def predict(request, phrase):
    prediction = predictor.predict(phrase)
    return HttpResponse(json.dumps(prediction))
