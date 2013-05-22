import json

from django.test import TestCase
from django.test.client import Client
from django.http import HttpResponse

from hillbilly.guns.models import Gun


class GunAsDictTest(TestCase):

    def test_as_dict(self):
        gun = Gun.objects.create(name='M16', caliber='.65')
        self.assertEquals({"caliber": ".65",
                           "id": gun.id,
                           "name": "M16"},
                          gun.as_dict())

class GunAsJSONTest(TestCase):

    def test_as_dict(self):
        gun = Gun.objects.create(name='M16', caliber='.65')
        self.assertEquals('{"caliber": ".65", "id": %s, "name": "M16"}' % gun.id,
                          gun.as_json())


class GetGunsTest(TestCase):

    def test_empty_guns(self):
        client = Client()
        response = client.get('/guns/')
        self.assertIsInstance(response, HttpResponse)
        self.assertEquals(('Content-Type', 'application/json'),
                           response._headers['content-type'])

    def test_one_gun(self):
        gun = Gun.objects.create(name='M16', caliber='.65')

        client = Client()
        response = client.get('/guns/')

        self.assertEquals({'data': [{'id': gun.id,
                                     'name': 'M16',
                                     'caliber': '.65'}]},
                          json.loads(response.content))


    def test_one_gun(self):
        m16 = Gun.objects.create(name='M16', caliber='.65')
        luger = Gun.objects.create(name='Luger', caliber='.35')

        client = Client()
        response = client.get('/guns/')

        m16 = {'id': m16.id, 'name': 'M16', 'caliber': '.65'}
        luger = {'id': luger.id, 'name': 'Luger', 'caliber': '.35'}
        data = json.loads(response.content)['data']

        self.assertTrue(m16 in data)
        self.assertTrue(luger in data)


class GetGunTest(TestCase):

    def test_gun_by_id(self):
        m16 = Gun.objects.create(name='M16', caliber='.65')

        client = Client()
        response = client.get('/guns/%s/' % m16.id)

        self.assertEquals({'id': m16.id,
                           'name': 'M16',
                           'caliber': '.65'},
                          json.loads(response.content))


    def test_gun_doesnt_exist(self):
        client = Client()
        response = client.get('/guns/7654/')
        self.assertEquals(404, response.status_code)


class CreateGunTest(TestCase):

    def test_create_gun_returns_resource(self):
        client = Client()
        response = client.post('/guns/', {'name': 'Smith & Wesson',
                                          'caliber': '.37'})

        smith_and_wesson_json = json.loads(response.content)

        self.assertEquals({'id': smith_and_wesson_json['id'],
                           'name': 'Smith & Wesson',
                           'caliber': '.37'},
                          smith_and_wesson_json)

    def test_create_gun_creates_instance(self):
        client = Client()
        response = client.post('/guns/', {'name': 'Smith & Wesson',
                                          'caliber': '.37'})

        smith_and_wesson_json = json.loads(response.content)

        smith_and_wesson = Gun.objects.get(id=smith_and_wesson_json['id'])
        self.assertEquals('Smith & Wesson', smith_and_wesson.name)
        self.assertEquals('.37', smith_and_wesson.caliber)
