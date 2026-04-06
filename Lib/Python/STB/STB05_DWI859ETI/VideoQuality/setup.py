from setuptools import setup
from Cython.Build import cythonize

setup(
    name="video_metrics",
    ext_modules=cythonize("Video_metrics_robot.py", compiler_directives={'language_level': "3"}),
)
