from setuptools import setup, find_packages

setup(
      name="idmodels",
      author = "Ed Rial",
      version = "0.1",
      description='Python Modelling and Analysis of Undulators, using Radia, and wrapped Radia',
      dependency_links=['http://github.com/ochubar/Radia/tarball/master#egg=package-1.0&subdirectory=env/radia_python',
                        'http://github.com/eddrial/wradia/tarball/master#egg=package-1.0'],
      packages = find_packages()#,
#      install_requires = ['some-pkg @ git+https://github.com/eddrial/wRadia@master']#,
#                          'radia',
#                          ''],
#     # package_data={'': ['radia_py3_7_x86_64.so']},
      )
#
