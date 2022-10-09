from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(), 
    # Tells Python what package directories to include. find_packages() finds these directories automatically
    include_package_data=True,
    # To include other files, such as the static and templates directories, include_package_data is set. 
    # Python needs another file named MANIFEST.in to tell what this other data is.
    install_requires=[
        'flask',
    ],
)

# Use 'pip install -e .' to install your project in the virtual environment.