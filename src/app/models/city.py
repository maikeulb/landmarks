from flask import url_for
from app.extensions import db
from app.models.mixins import PaginatedAPIMixin


class City(PaginatedAPIMixin, db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    state = db.Column(db.String(50))

    landmarks = db.relationship(
        'Landmark'
    )

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'number_of_landmarks': len(self.landmarks),
            '_links': {
                'self': url_for('api.get_city', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'state']:
            if field in data:
                setattr(self, field, data[field])
