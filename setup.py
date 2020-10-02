from setuptools import setup, find_packages

setup(name='webapi',
      version='0.0.1',
      description='Web APIs',
      packages=find_packages(),
      # package_data={'': ['utils/*.sh', 'utils/*.jar']},
      install_requires=[
            'beautifulsoup4',
            'requests'
      ],
      include_package_data=True,
      zip_safe=False)
