import os
import click
from app.extensions import db
from app.models import Borough, Landmark
from flask import current_app
from datetime import date

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def register(app):
    @app.cli.command("seed-db")
    def seed_db():
        print('Starting DB seed')
        db.drop_all()
        db.create_all()

        print('Adding Boroughs')
        manhattan = Borough(name="Manhattan")
        brooklyn = Borough(name="Brooklyn")
        queens = Borough(name="Queens")
        bronx = Borough(name="Bronx")
        staten_island = Borough(name="Staten Island")

        db.session.add(manhattan)
        db.session.add(brooklyn)
        db.session.add(queens)
        db.session.add(bronx)
        db.session.add(staten_island)

        print('Adding Landmarks')
        wall_street = Landmark(name="1 Wall Street Building",
                               description="Art-Deco-style skyscraper designed by Ralph Walker,originally built for the Irving Trust Company.",
                               date_designated=date(2001, 3, 6),
                               borough_id=1)
        woolworth = Landmark(name="Woolworth Building",
                             description="Designed in the neo-Gothic style by architect Cass Gilbert. Originally designed to be 420 feet high, the building was eventually elevated to 792 feet.",
                             date_designated=date(1983, 12, 6),
                             borough_id=1)
        harlem = Landmark(name="Harlem CourtHouse",
                          description="Designed by Thom & Wilson in the Romanesque Revival style.",
                          date_designated=date(1967, 8, 2),
                          borough_id=1)
        regiment_armory = Landmark(name="14th Regiment Armory",
                                   description="Designed by William Mundell,this building is a Brick and stone caste-like structure completed in 1893, and designated to be reminiscent of medievel military structures in Europe.",
                                   date_designated=date(1998, 4, 14),
                                   borough_id=2)
        first_reformed = Landmark(name="First Reformed Church",
                                  description="The church has an early romanesque structure that wasdesignated by Sidney J Young and built by Anders Peterson.",
                                  date_designated=date(1996, 1, 30),
                                  borough_id=3)
        flushing = Landmark(name="Flushing Town Hall",
                            description="A style of architecture that originated in Germany, Rundbogenstila.",
                            date_designated=date(1968, 7, 30),
                            borough_id=3)
        high_bridge = Landmark(name="High Bridge",
                               description="The oldest bridge in New York City, having originallyopened as part of the Croton Aqueduct in 1848 and reopened as a pedestrian walkway in 2015.",
                               date_designated=date(1970, 11, 10),
                               borough_id=4)
        curtis_high = Landmark(name="Curtis High School",
                               description="It was founded on February 9 1994, the first high school on Staten Island.",
                               date_designated=date(1982, 10, 12),
                               borough_id=5)
        pendleton = Landmark(name="Pendleton Place House",
                             description="It was built in 1860, and is a 3-story picturesque Italianate villa style frame dwelling with a multi-gabled roof.",
                             date_designated=date(2006, 3, 14),
                             borough_id=5)

        db.session.add(wall_street)
        db.session.add(woolworth)
        db.session.add(harlem)
        db.session.add(regiment_armory)
        db.session.add(first_reformed)
        db.session.add(flushing)
        db.session.add(high_bridge)
        db.session.add(curtis_high)
        db.session.add(pendleton)

        db.session.commit()
        print('DB seed complete')

    @app.cli.command("test")
    def test():
        import pytest
        rv = pytest.main([TEST_PATH, '--verbose'])
        exit(rv)
