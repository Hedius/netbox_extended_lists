from setuptools import find_packages, setup

from netbox_extended_lists import version

setup(
    name='netbox-extended-lists',
    version=version,
    description='Adds extended views / lists to NetBox.',
    url='https://github.com/Hedius/netbox_extended_lists',
    author='Hedius & pheeef',
    author_email='git@hedius.eu',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
