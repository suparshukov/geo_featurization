from . import geo_utils


class GeoObject:

    def __init__(self, name, shp_file, filters, region_of_interest):

        self.name = name
        self._region_of_interest = region_of_interest
        self._shp_file = shp_file
        self._filters = filters
        self._load_layer()

    def _load_layer(self):
        layer = geo_utils.load_shp(self._shp_file)
        layer = layer[layer.intersects(self._region_of_interest.unary_union)]
        row_mask = layer[list(self._filters.keys())].isin(self._filters).all(1)
        self.layer = layer[row_mask]


class FeaturizedLayer:

    def __init__(self, layer):
        self.layer = layer

    @classmethod
    def from_shp(cls, layer_shp):
        layer = geo_utils.load_shp(layer_shp)
        return cls(layer)

    @classmethod
    def from_hexagons(cls, region_of_interest_shp, hexagons_resolution=8):
        region_of_interest = geo_utils.load_shp(region_of_interest_shp)
        layer = geo_utils.get_hexagons_for_region(region_of_interest, hexagons_resolution)
        return cls(layer)

    def featurize(self, geo_object, operation):
        pass
