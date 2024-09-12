from pathlib import Path
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
    