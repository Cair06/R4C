import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from robots.forms import RobotForm


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        try:
            json_data: dict = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

        form = RobotForm(json_data)
        if form.is_valid():
            robot = form.save()
            return JsonResponse({
                'msg': 'Robot successfully added',
                'id': robot.id,
                'model': robot.model,
                'version': robot.version,
                'created': robot.created.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
