import geopandas as gpd

from . import geo_utils


class GeoObject(object):
    """Spatial object layer, which is used to calculate features

    Attributes:
        name: Name (alias) of spatial objects layer (for example, bus station, supermarket etc.).
        shp_path: Path to a shape file where the spatial objects layer is stored.
        filters: .
        region_of_interest: .
    """

    def __init__(self,
                 name: str,
                 shp_file: str,
                 filters: dict[str, str],
                 region_of_interest: gpd.GeoSeries):
        """Inits GeoObject"""
        self.name = name
        self._region_of_interest = region_of_interest
        self._shp_file = shp_file
        self._filters = filters

    def load_layer(self) -> gpd.GeoDataFrame:
        """

        Returns:
            Layer of spatial objects with filters applied

        """
        layer = geo_utils.load_shp(self._shp_file)
        layer = layer[layer.intersects(self._region_of_interest.unary_union)]
        row_mask = layer[list(self._filters.keys())].isin(self._filters).all(1)
        layer = layer[row_mask]

        return layer


class FeaturizedLayer(object):
    """Layer of spatial objects for which features need to be calculated

    Attributes:
        layer (gpd.GeoDataFrame):
    """

    def __init__(self, layer: gpd.GeoDataFrame):
        """Inits FeaturizedLayer"""
        self.layer = layer

    @classmethod
    def from_shp(cls, shp_path: str):
        """
        Load spatial objects from a shape file.

        Args:
            shp_path (string): Path to a shape file.

        Returns:
            Layer of spatial objects to featurize
        """
        layer = geo_utils.load_shp(shp_path)

        return cls(layer)

    @classmethod
    def from_hexagons(cls, region_of_interest_shp: str, hexagons_resolution: int = 8):
        """
        Create spatial objects layer based on geometry of a region of interest and H3 grid resolution.

        Args:
            region_of_interest_shp (str): Path to a shape file with a region of interest geometry
            hexagons_resolution (int):

        Returns:
            Layer of spatial objects to featurize
        """

        region_of_interest = geo_utils.load_shp(region_of_interest_shp)
        layer = geo_utils.get_h3_hexagons_for_region(
            region_of_interest, hexagons_resolution
        )

        return cls(layer)
