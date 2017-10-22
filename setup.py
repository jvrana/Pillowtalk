import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


tests_require = [
    'pytest',
    'pytest-runner',
    'python-coveralls',
    'pytest-pep8'
]

install_requires = [
    'inflection',
    'marshmallow'
]

classifiers = [
                  # How mature is this project? Common values are
                  #   3 - Alpha
                  #   4 - Beta
                  #   5 - Production/Stable
                  'Development Status :: 3 - Alpha',

                  # Indicate who your project is intended for
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',

                  # Pick your license as you wish (should match "license" above)
                  'License :: OSI Approved :: MIT License',

                  # Specify the Python versions you support here. In particular, ensure
                  # that you indicate whether you support Python 2, Python 3 or both.
                  "Programming Language:: Python:: 3.4",
                  "Programming Language:: Python:: 3.5",
                  "Programming Language:: Python:: 3.6",
                  "Programming Language:: Python:: 3.7",
              ],

setup(
        name='marshpillow',
        version='1.0',
        packages=['marshpillow'],
        url='https://github.com/jvrana/marshpillow',
        license='MIT',
        author='Justin Dane Vrana',
        author_email='justin.vrana@gmail.com',
        keywords='serialization marshmallow deserialization orm api-wrapper api',
        description='Intuitive API wrapper framework using marshmallow',
        long_description=read('README.md'),
        install_requires=install_requires,
        python_requires='>=3.4',
        tests_require=tests_require,
        classifiers=classifiers
)
