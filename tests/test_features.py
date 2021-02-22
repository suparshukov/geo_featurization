import os
import sys


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src/geo_featurization/")
    ),
)


def test_sample():

    assert 0 == 0
