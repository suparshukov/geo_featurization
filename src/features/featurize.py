from ..geo.geo_utils import count_contains

class Featurization:

    def __init__(self, name, operation, geo_object, params=None):

        self.name = name
        self.operation = operation
        self.geo_object = geo_object
        self.params = params


class GeoFeaturizer:

    def __init__(self, featurized_layer, geo_objects, featurizations):

        self.featurized_layer = featurized_layer
        self.geo_objects = geo_objects
        self.featurizations = featurizations

    def featurize(self):

        for featurization in self.featurizations:

            if self.geo_objects[featurization.geo_object].layer.shape[0] == 0:
                self.featurized_layer.layer[featurization.name] = 0
                continue

            if featurization.operation == 'count_contains':
                self.featurized_layer.layer = count_contains(self.featurized_layer.layer,
                                                             self.geo_objects[featurization.geo_object],
                                                             featurization.name)
