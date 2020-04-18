from ..geo.geo_operation import count_contains, count_intersects, distance_to_nearest


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

            geo_object_layer = self.geo_objects[featurization.geo_object].load_layer()

            if geo_object_layer.shape[0] == 0:
                self.featurized_layer.layer[featurization.name] = 0
                continue

            if featurization.operation == 'count_contains':
                self.featurized_layer.layer = count_contains(self.featurized_layer.layer,
                                                             geo_object_layer,
                                                             featurization.name)
            if featurization.operation == 'count_intersects':
                self.featurized_layer.layer = count_intersects(self.featurized_layer.layer,
                                                               geo_object_layer,
                                                               featurization.name)
            if featurization.operation == 'distance_to_nearest':
                self.featurized_layer.layer = distance_to_nearest(self.featurized_layer.layer,
                                                                  geo_object_layer,
                                                                  featurization.name)
