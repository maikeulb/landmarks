from flask import url_for
from app.extensions import db
from app.models.mixins import PaginatedAPIMixin


class Landmark(PaginatedAPIMixin, db.Model):
    __tablename__ = 'landmarks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(140))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))

    city = db.relationship(
        'City'
    )

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            '_links': {
                'self': url_for('api.get_landmark', cityId=self.city_id, 
                                id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
