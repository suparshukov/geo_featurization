import keplergl

def draw_layers_kepler(hexagons_gdf, layers_dict):
    map_kepler = keplergl.KeplerGl(height=800)
    for layer_name, geo in layers_dict.items():
        map_kepler.add_data(geo, name=layer_name);
    map_kepler.add_data(data=hexagons_gdf[['geometry']], name='hexagons')

    return map_kepler