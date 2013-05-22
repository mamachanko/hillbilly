import json

from django.db import models


class Gun(models.Model):
    name = models.CharField(max_length=200)
    caliber = models.CharField(max_length=200)

    def as_dict(self):
        return {'id': self.id,
               'name': self.name,
               'caliber': self.caliber}

    def as_json(self):
        return json.dumps(self.as_dict())

    def as_html(self):
        return ('<ol>'
                '<li>id: %(id)s</li>'
                '<li>name: %(name)s</li>'
                '<li>caliber: %(caliber)s</li>'
                '</ol>' % self.as_dict())
