from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['ros_counteruav'],
    scripts=['scripts/data_receiver.py','scripts/fake_data_sender.py', 'scripts/try_data_analyzer.py', 'scripts/web_visualizer.py'],
    package_dir={'': 'src'}
)

setup(**d)