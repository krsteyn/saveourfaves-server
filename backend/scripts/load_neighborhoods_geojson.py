import json
import django
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'carebackend.settings'
sys.path.append(os.path.dirname(__file__) + '/..')
django.setup()
from places.models import Neighborhood, NeighborhoodEntry, Place, Area
from django.contrib.gis.geos import Polygon
import pandas as pd
from shapely.geometry import Polygon as ShapelyPolygon

insert_if_not_found = True
fn = os.path.join(os.path.dirname(__file__), './munic.geojson')

with open(fn) as f:
    data = json.load(f)

for feature in data["features"]:
    print("Processing neigherhood >>>> ", feature["properties"]["MUNICNAME"])
    try:
        n = Neighborhood.objects.get(key=feature["id"])
    except Neighborhood.DoesNotExist:
        if insert_if_not_found:
            n = Neighborhood(name=feature["properties"]["MUNICNAME"])
            n.key = feature["id"]
        else:
            print("No DB Key match and not inserting, continuing...")
            continue
    cords = json.dumps(feature["geometry"]["coordinates"])
    if cords.startswith('[[['):
        cords = cords[1:-1]
    if not cords.startswith('[['):
        cords = '[%s]' % cords
    geo_json = json.loads(cords)
    n.bounds = Polygon(geo_json)
    poly = ShapelyPolygon(geo_json)
    centroid = poly.centroid
    lat = centroid.y
    lng = centroid.x
    n.lat = lat
    n.lng = lng
    n.area = Area.objects.get(key=feature["properties"]["PROVINCE"])
    n.rank = None
    n.save()
