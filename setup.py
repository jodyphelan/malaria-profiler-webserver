from setuptools import find_packages, setup
import os
setup(
    name='malaria-profiler-webserver',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # scripts= ["scripts/%s" % x for x in os.listdir("scripts")],
)
