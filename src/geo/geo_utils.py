import geopandas as gpd
import json
import pandas as pd
import shapely

from h3 import h3


def load_shp(filename):

    layer = gpd.read_file(filename)

    return layer


def get_geo_objects(geo_objects_config, path_to_data, region_of_interest):

    geo_objects = dict()

    for geo_object in geo_objects_config:
        geo_object_name = list(geo_object.keys())[0]
        shp_filename = geo_object[geo_object_name]['shp']
        filters = geo_object[geo_object_name]['filters']
        layer = load_shp(path_to_data + '/' + shp_filename)
        layer = layer[layer.intersects(region_of_interest.unary_union)]
        row_mask = layer[list(filters.keys())].isin(filters).all(1)
        layer = layer[row_mask]
        geo_objects[geo_object_name] = layer

    return geo_objects


def get_hexagons_for_region(region_of_interest, resolution):

    boundary = shapely.ops.cascaded_union(region_of_interest['geometry'])
    if boundary.geom_type == 'MultiPolygon':
        region_of_interest_json = (gpd.GeoSeries(
            list(shapely.ops.cascaded_union(region_of_interest['geometry']))).to_json())
    elif boundary.geom_type == 'Polygon':
        region_of_interest_json = (gpd.GeoSeries(
            shapely.ops.cascaded_union(region_of_interest['geometry'])).to_json())

    hexagons = pd.DataFrame()
    for feature in json.loads(region_of_interest_json)['features']:
        hexagons_part = pd.DataFrame(h3.polyfill(geo_json=feature['geometry'], res=resolution,
                                                 geo_json_conformant=True),
                                     columns=['hex_id'])
        hexagons = hexagons.append(hexagons_part, ignore_index=True)

    hexagons['geometry'] = (hexagons['hex_id']
                            .apply(lambda h: shapely.geometry.asPolygon(h3.h3_to_geo_boundary(h, geo_json=True))))
    hexagons_gdf = gpd.GeoDataFrame(hexagons, geometry='geometry')

    return hexagons_gdf


def save_geo_objects():
    pass

def save_layer():
    pass

def get_geo_object():
    pass


def count_contains(feat_layer, geo_object, name):

    feat_layer.reset_index(drop=True, inplace=True)
    geo_object.layer.reset_index(drop=True, inplace=True)
    dfsjoin = gpd.sjoin(feat_layer, geo_object.layer, op='contains', how='left')
    agg_df = dfsjoin.groupby(level=0).agg({'index_right': 'count'})
    agg_df.rename({'index_right': name}, axis=1, inplace=True)
    feat_layer = feat_layer.merge(agg_df, how='left', left_index=True, right_index=True)

    return feat_layer



