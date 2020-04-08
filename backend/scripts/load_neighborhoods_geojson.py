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

fl = sys.argv[1]
area_to_use = sys.argv[2]

insert_if_not_found = sys.argv[3] == 'yes' if len(sys.argv) > 3 else False
area = Area.objects.get(key=area_to_use)

with open('./munic.geojson') as f:
    data = json.load(f)

for feature in data["features"]:
    print("Processing", json.dumps(feature))
    try:
        n = Neighborhood.objects.get(key=feature["id"])
    except Neighborhood.DoesNotExist:
        if insert_if_not_found:
            n = Neighborhood(name=feature["properties"]["MUNICNAME"])
            n.key = feature["id"]
        else:
            print("No DB Key match and not inserting, continuing...")
            continue
    n.bounds = Polygon(feature)
    poly = ShapelyPolygon(feature)
    centroid = poly.centroid
    lat = centroid.y
    lng = centroid.x
    n.lat = lat
    n.lng = lng
    n.area = feature["properties"]["PROVINCE"]
    n.rank = None
    n.save()
