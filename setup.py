from setuptools import setup
setup(
    name = 'ticket_cli',
    version = '0.1.0',
    packages = ['ticket_cli'],
    entry_points = {
        'console_scripts': [
            'ticket_cli = ticket_cli.__main__:main'
        ]
})
