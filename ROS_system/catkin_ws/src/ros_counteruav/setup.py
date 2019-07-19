from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['ros_counteruav'],
    scripts=['listener.py','talker.py'],
    package_dir={'': 'scripts'}
)

setup(**d)