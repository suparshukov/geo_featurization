from . import geo_utils


class GeoObject(object):
    """

    Attributes:
        name: .
        shp_file: .
        filters: .
        region_of_interest: .
    """

    def __init__(self, name, shp_file, filters, region_of_interest):
        """Inits GeoObject."""
        self.name = name
        self._region_of_interest = region_of_interest
        self._shp_file = shp_file
        self._filters = filters

    def load_layer(self):
        """

        Returns:

        Raises:

        """
        layer = geo_utils.load_shp(self._shp_file)
        layer = layer[layer.intersects(self._region_of_interest.unary_union)]
        row_mask = layer[list(self._filters.keys())].isin(self._filters).all(1)
        layer = layer[row_mask]

        return layer


class FeaturizedLayer(object):
    """

    Attributes:
        layer: .
    """

    def __init__(self, layer):
        """Inits FeaturizedLayer."""
        self.layer = layer

    @classmethod
    def from_shp(cls, layer_shp):
        """

        Args:
            layer_shp (): .

        Returns:

        Raises:

        """
        layer = geo_utils.load_shp(layer_shp)
        return cls(layer)

    @classmethod
    def from_hexagons(cls, region_of_interest_shp, hexagons_resolution=8):
        """

        Args:
            region_of_interest_shp ():
            hexagons_resolution ():

        Returns:

        Raises:

        """

        region_of_interest = geo_utils.load_shp(region_of_interest_shp)
        layer = geo_utils.get_h3_hexagons_for_region(
            region_of_interest, hexagons_resolution
        )

        return cls(layer)
