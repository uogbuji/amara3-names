from setuptools import setup, find_packages

REQUIREMENTS = ['nameparser']
TEST_REQUIREMENTS = ['nose']

setup(
    name='amara3.names',
    packages=find_packages(),
    version='0.1.2',
    description='Tools to handle human names (and organization names). Credit to https://www.github.com/rliebz/whoswho by Robert Liebowitz <rliebz@gmail.com>',
    author='Uche Ogbuji',
    author_email='uche@ogbuji.net',
    url='http://uche.ogbuji.net',
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ),
    keywords=['naturallanguage', 'name', 'match', 'parser']
)
