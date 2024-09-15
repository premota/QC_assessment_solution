import os
from pathlib import Path
import pickle
import yaml

from box import Box
import sys

from utils.exception import CustomException



def read_yaml(path: Path) -> Box:
    """
    Reads a YAML file and returns its content as a Box object.

    Parameters:
    ----------
    path : Path
        The file path of the YAML configuration file.

    Returns:
    -------
    Box:
        A Box object containing the parsed data from the YAML file.
    """
    try:
        with open(path) as file:
            data = yaml.safe_load(file)
            return Box(data)
    except Exception as e:
        raise CustomException(e,sys)


def save_to_pickle(obj_path: Path, obj):
    """
    Saves a Python object as a pickle file at the specified path.

    Parameters:
    ----------
    obj_path : Path
        The path where the pickle file will be saved.
    obj : object
        The Python object to be serialized and saved.

    Returns:
    -------
    None
    """
    try:
        # first create folder if absent
        dir_path = os.path.dirname(obj_path)
        os.makedirs(dir_path, exist_ok=True)

        # create pickle
        with open(obj_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise CustomException(e,sys)
    
    
def load_pickle(object_path:Path):
    """
    Loads a Pickle object at the specified path.

    Parameters:
    ----------
    obj_path : Path
        The path where the pickle file has beeen saved.
    obj : object
        The Pickle object to be extracted.

    Returns:
    -------
    None
    """
    try:
        with open(object_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomException(e,sys)