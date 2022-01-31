from distutils.core import setup

setup(
    name='python-card-games',
    version='1.0',
    packages=['cardgames', 'cardgames.games', 'cardgames.components'], # list packages (folders) not files
    license='',
    author='thomas',
    author_email='thomas@fultondesigns.co.uk',
    description='',
    long_description = open('README.txt').read(),
    url='https://github.com/Thomas-Fulton/python-card-games.git',
)
