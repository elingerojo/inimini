import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .postpone import postpone


@require_POST
@csrf_exempt
def hook(request):

  event = json.loads(request.body)
  # Peek payload
  print('event = ', event)

  # Your fast code goes here. Like extract relevant data
  payload = event

  # When ready call your slow code
  long_process(payload)

  # Acknowledge event to originator
  return HttpResponse(status=200)

@postpone
def long_process(payload):

    # Your slow code goes here, like database request

    # Done. Nothing else to do and none to inform
    return
