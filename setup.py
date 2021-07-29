from setuptools import setup
setup(
    name = 'clitesting',
    version = '0.1.0',
    packages = ['clitesting'],
    entry_points = {
        'console_scripts': [
            'clitesting = clitesting.__main__:main'
        ]
})
