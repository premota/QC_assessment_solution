import os
from pathlib import Path
import pickle
import yaml

from box import Box
import sys

from utils.exception import CustomException



def read_yaml(path: Path) -> Box:
    try:
        with open(path) as file:
            data = yaml.safe_load(file)
            return Box(data)
    except Exception as e:
        raise CustomException(e,sys)


def save_to_pickle(obj_path: Path, obj):
    try:
        # first create folder if absent
        dir_path = os.path.dirname(obj_path)
        os.makedirs(dir_path, exist_ok=True)

        # create pickle
        with open(obj_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise CustomException(e,sys)