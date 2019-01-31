from setuptools import setup

setup(
 name="pygtop",
 version="2.1.4",
 description="A Python wrapper for the Guide to PHARMACOLOGY API. It provides \
 a Python interface for access to the GtoP database.",
 url="https://pygtop.readthedocs.org",
 author="Sam Ireland",
 author_email="Sam.Ireland@ed.ac.uk",
 license="MIT",
 classifiers=[
  "Development Status :: 4 - Beta",
  "Intended Audience :: Science/Research",
  "License :: OSI Approved :: MIT License",
  "Topic :: Scientific/Engineering :: Chemistry",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.0",
  "Programming Language :: Python :: 3.1",
  "Programming Language :: Python :: 3.2",
  "Programming Language :: Python :: 3.3",
  "Programming Language :: Python :: 3.4",
  "Programming Language :: Python :: 3.5",
  "Programming Language :: Python :: 3.6",
  "Programming Language :: Python :: 3.7",

 ],
 keywords="pharmacology drugs chemistry bioinformatics",
 packages=["pygtop"],
 install_requires=["requests", "molecupy"]
)
