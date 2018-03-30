from flask import url_for
from app.extensions import db
from app.models.mixins import PaginatedAPIMixin


class Borough(PaginatedAPIMixin, db.Model):
    __tablename__ = 'boroughs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    landmarks = db.relationship(
        'Landmark'
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'numberOfLandmarks': len(self.landmarks),
            '_links': {
                'self': url_for('api.get_borough', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])
