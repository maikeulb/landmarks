from flask import url_for
from app.extensions import db
from app.models.mixins import PaginatedAPIMixin


class Landmark(PaginatedAPIMixin, db.Model):
    __tablename__ = 'landmarks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(400))
    date_designated = db.Column(db.DateTime, nullable=True)
    borough_id = db.Column(db.Integer, db.ForeignKey('boroughs.id'))

    borough = db.relationship(
        'Borough'
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'date_designated': self.date_designated,
            'description': self.description,
            '_links': {
                'self': url_for('api.get_landmark', boroughId=self.borough_id,
                                id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'date_designated', 'description']:
            if field in data:
                setattr(self, field, data[field])
