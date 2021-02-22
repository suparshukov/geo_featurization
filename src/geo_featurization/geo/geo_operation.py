import geopandas as gpd

from .geo_utils import calc_dist_from_points_to_nearest_point


def count_contains(feat_layer, geo_object, name):
    """

    Args:
        feat_layer:
        geo_object:
        name:

    Returns:

    Raises:

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


def count_intersects(feat_layer, geo_object, name):
    """

    Args:
        feat_layer:
        geo_object:
        name:

    Returns:

    Raises:

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


def distance_to_nearest(feat_layer, geo_object, name):
    """

    Args:
        feat_layer:
        geo_object:
        name:

    Returns:

    Raises:

    """

    if (feat_layer.shape[0] == 0) or (geo_object.shape[0] == 0):
        return feat_layer

    # TODO: pass feat_layer geometry field instead? GeoSeries
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
