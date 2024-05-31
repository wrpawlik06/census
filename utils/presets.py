def get_slider_ranges(preset:str):

    if preset == 'no_selection':
        slider_ranges = {'median_price_range': (0,1600000),
        "children_16_percentage_range": (0.0, 0.40),
        "children_4_percentage_range":  (0.0, 0.40),
        "population_density_range": (0,21589)}
        
        return slider_ranges

