from setuptools import setup, find_packages
from typing import List

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


editable = "-e ."
def find_requirements(file_path: str)-> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if editable in requirements:
            requirements.remove(editable)




__version__ = "0.0.1"

REPO_NAME = "QC_assessment_solution"
AUTHOR_GITHUB_USER_NAME = "premota"
SRC_REPO = "Classfication"

setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_GITHUB_USER_NAME,
    description="label prediction (1 or 0)",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_GITHUB_USER_NAME}/{REPO_NAME}",
    packages=find_packages(),
    install_require = find_requirements("requirements.txt")

)