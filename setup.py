from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='mro-migrator',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Tool to migrate MRO conda environments to use Anaconda R",
    author="Anaconda, Inc.",
    author_email='conda@anaconda.com',
    url='https://github.com/continuumio/mro-migrator',
    packages=['mro_migrator'],
    entry_points={
        'console_scripts': [
            'mro_migrator=mro_migrator.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='mro-migrator',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
