# placeholder for additional utils modified from grasshopper components
from honeybee.model import Model


def make_hb_model_json(model):
    return model.to_hbjson(folder='temp_assets', indent=3)
