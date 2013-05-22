import json

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.base import View

from hillbilly.guns.models import Gun


def guns(request):
    if request.method == 'POST':
        return post_gun(request)

    if request.method == 'GET':
        return get_all_guns()

def post_gun(request):
    name = request.POST.get('name')
    caliber = request.POST.get('caliber')

    gun = Gun(name=name, caliber=caliber)
    gun.save()

    return HttpResponse(gun.as_json(), content_type='application/json')

def get_all_guns():
    guns = []
    for gun in Gun.objects.all():
        guns.append(gun.as_dict())
    return HttpResponse(json.dumps({'data': guns}),
                        content_type='application/json')

def get_gun_by_id(request, gun_id):
    try:
        gun = Gun.objects.get(id=gun_id)
    except Gun.DoesNotExist:
        return HttpResponseNotFound()
    else:
        return HttpResponse(gun.as_json(), content_type='application/json')


class Guns(View):

    def get(self, request):
        return get_all_guns()

    def post(self, request):
        return post_gun(request)
