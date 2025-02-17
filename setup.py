import codecs

from setuptools import Extension, setup

sources = [
    "libmgrs/mgrs.c",
    "libmgrs/utm.c",
    "libmgrs/ups.c",
    "libmgrs/tranmerc.c",
    "libmgrs/polarst.c",
]


mgrs = Extension(
    "libmgrs",
    sources=sources,
    define_macros=None,
    include_dirs=["./libmgrs"],
    libraries=None,
    library_dirs=None,
)


with codecs.open("./README.rst", encoding="utf-8") as f:
    readme_text = f.read()

setup(
    name="mgrs",
    version="2.0",
    description="MGRS coordinate conversion for Python",
    license="MIT",
    keywords="gis coordinate conversion",
    author="Howard Butler, Gabriel Belouze",
    author_email="howard@hobu.co, gabriel@belouze.com",
    maintainer="Gabriel Belouze",
    maintainer_email="gabriel@belouze.com",
    url="https://github.com/gbelouze/mgrs",
    long_description=readme_text,
    long_description_content_type="text/x-rst",
    ext_modules=[mgrs],
    install_requires=["packaging"],
    packages=["mgrs"],
    test_suite="tests.test_suite",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Database",
    ],
)
