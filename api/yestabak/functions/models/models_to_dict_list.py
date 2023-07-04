from sqlalchemy.orm import class_mapper


def model_to_dict(model):
    model_map = class_mapper(model.__class__)
    model_dict = {}
    for column in model_map.columns:
        model_dict[column.name] = getattr(model, column.name)
    return model_dict


def models_to_dict_list(models):
    return [model_to_dict(model) for model in models]
