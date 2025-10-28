from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "C:\\Users\\stijn\\OneDrive - Corderius College\\5e 6e jaar PWS\\PWS repository\\competition_bot_cy.pyx",
        compiler_directives={"language_level": "3"},
    )
)
