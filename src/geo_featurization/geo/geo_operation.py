import geopandas as gpd

from .geo_utils import calc_dist_from_points_to_nearest_point


def count_contains(feat_layer: gpd.GeoDataFrame,
                   geo_object: gpd.GeoDataFrame,
                   name: str) -> gpd.GeoDataFrame:
    """Count the number of objects inside the objects of the input layer

    Args:
        feat_layer: a layer to add features to
        geo_object: a layer of objects, the number of which
                    within the objects of the source layer we want to count
        name: a name for a result field

    Returns:
        An input layer with new feature added - number of objects of other layer inside
    """

    # TODO: check geometry types
    feat_layer.reset_index(drop=True, inplace=True)
    geo_object.reset_index(drop=True, inplace=True)
    dfsjoin = gpd.sjoin(feat_layer, geo_object, op="contains", how="left")
    agg_df = dfsjoin.groupby(level=0).agg({"index_right": "count"})
    agg_df.rename({"index_right": name}, axis=1, inplace=True)
    feat_layer = feat_layer.merge(
        agg_df, how="left", left_index=True, right_index=True
    )

    return feat_layer


def count_intersects(feat_layer: gpd.GeoDataFrame,
                     geo_object: gpd.GeoDataFrame,
                     name: str) -> gpd.GeoDataFrame:
    """Count the number of intersections of objects with objects in the input layer

    Args:
        feat_layer: a layer to add features to
        geo_object: a layer of objects, the number of intersections of which
                    with the objects of the source layer we want to count
        name: a name for a result field

    Returns:
        An input layer with new feature added - number of intersected objects of other layer
    """

    # TODO: check geometry types
    feat_layer.reset_index(drop=True, inplace=True)
    geo_object.reset_index(drop=True, inplace=True)
    dfsjoin = gpd.sjoin(feat_layer, geo_object, op="intersects", how="left")
    agg_df = dfsjoin.groupby(level=0).agg({"index_right": "count"})
    agg_df.rename({"index_right": name}, axis=1, inplace=True)
    feat_layer = feat_layer.merge(
        agg_df, how="left", left_index=True, right_index=True
    )

    return feat_layer


def distance_to_nearest(feat_layer: gpd.GeoDataFrame,
                        geo_object: gpd.GeoDataFrame,
                        name: str) -> gpd.GeoDataFrame:
    """Calculate distances from objects in the input layer to the nearest objects in another layer

    Args:
        feat_layer: a layer to add features to
        geo_object: layer, to the closest objects of which from the objects
                    of the input layer we want to calculate the distances
        name: a name for a result field

    Returns:
        An input layer with new feature added - distance to the nearest object of other layer
    """

    if (feat_layer.shape[0] == 0) or (geo_object.shape[0] == 0):
        return feat_layer

    # TODO: pass feat_layer geometry field instead GeoSeries?
    layer = (
        feat_layer
        if feat_layer.iloc[0]["geometry"].geom_type == "Point"
        else feat_layer.centroid
    )
    points = (
        geo_object
        if geo_object.iloc[0]["geometry"].geom_type == "Point"
        else geo_object.centroid
    )

    dist_field_name = "dist_" + name
    print(type(layer), type(points))
    dist_gdf = calc_dist_from_points_to_nearest_point(
        layer, points, dist_field_name
    )

    feat_layer = feat_layer.merge(
        dist_gdf[[dist_field_name]],
        how="left",
        left_index=True,
        right_index=True,
    )

    return feat_layer
