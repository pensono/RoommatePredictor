import json
import random
import emoji
import logging

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from . import predictor


def index(request):
    template = loader.get_template('index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def test(request):
    names = predictor.get_options()
    template = loader.get_template('test.html')

    phrases = load_phrases()

    annotated_phrases = []

    for i in range(25):
        index = random.randint(0, len(phrases)-1)
        annotated_phrases.append({
            'text': phrases[index]['text'],
            'index': index,
            'number': i + 1
        })

    context = {
        'phrases': annotated_phrases,
        'options': names
    }

    return HttpResponse(template.render(context, request))


def load_phrases():
    names = predictor.get_options()
    with open('/data/group_chat.json', 'r', encoding='utf-8') as phrase_file:
        phrases = json.load(phrase_file)
        phrases = [phrase for phrase in phrases if phrase['sender'] in names]
    return phrases


logger = logging.getLogger('predictor')


@csrf_exempt  # Not a best practice, but gets the job done
def results(request):
    phrases = load_phrases()

    annotated_phrases = []
    score = 0
    for index in request.POST:
        actual = phrases[int(index)]['sender']
        guess = request.POST.get(index)
        correct = guess == actual
        if correct:
            score += 1
        annotated_phrases.append({
            'emoji': emoji.emojize(':white_check_mark:' if correct else ':x:', use_aliases=True),
            'text': phrases[int(index)]['text'],
            'guess': guess,
            'actual': actual,
        })

    context = {
        'phrases': annotated_phrases,
        'correct': score,
        'total': len(request.POST),
        'percent': f"{100.0 * score / len(request.POST):.0f}"
    }

    logger.info(context)

    template = loader.get_template('results.html')
    return HttpResponse(template.render(context, request))


def predict(request, phrase):
    prediction = predictor.predict(phrase)
    return HttpResponse(json.dumps(prediction))
