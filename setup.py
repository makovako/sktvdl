from setuptools import setup

setup(name='sktvdl',
      version='0.1',
      description='Downloader for video archives of slovak televisions',
      url='#',
      author='Marek Valko',
      author_email='',
      license='MIT',
      packages=['sktvdl'],
      zip_safe=False,
      entry_points={
          'console_scripts' : [
              'sktvdl = sktvdl:main'
          ]
      },
      install_requires=[
        'certifi>=2020.4.5.1',
        'chardet>=3.0.4',
        'idna>=2.9',
        'requests>=2.23.0',
        'selenium>=3.141.0',
        'urllib3>=1.25.8',
        'youtube-dl>=2020.3.24'
      ]
      )