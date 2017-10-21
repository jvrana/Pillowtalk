from distutils.core import setup

setup(
        name='marshpillow',
        version='0.0.1',
        packages=['marshpillow'],
        url='',
        license='',
        author='Justin Dane Vrana',
        author_email='justin.vrana@gmail.com',
        description='refactored trident',
        install_requires=["inflection", "marshmallow"],
        tests_require=['pytest'],
        setup_requires=[
            'pytest-runner', 'python-coveralls', 'pytest-pep8'
        ],
)