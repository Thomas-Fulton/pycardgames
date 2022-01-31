from distutils.core import setup

setup(
    name='pycardgames',
    version='0.1.0',
    packages=['cardgames', 'cardgames.games', 'cardgames.components'], # list packages (folders) not files
    license='MIT',
    author='thomas',
    author_email='thomas@fultondesigns.co.uk',
    description='',
    long_description=open('README.md').read(),
    url='https://github.com/Thomas-Fulton/python-card-games.git',
    entry_points={'console_scripts': [
        'pycardgames = cardgames.__main__:main'], }
)
