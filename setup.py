from setuptools import setup

setup(
    name='tempmailclient',
    version='0.1',
    description='10minutemail.org client',
    url='https://github.com/gabsdocompiuter/temp-mail',
    author='Gabriel Monteiro',
    author_email='gabsdocompiuter@gmail.com',
    license='MIT',
    packages=['tempmailclient'],
    zip_safe=False,
    install_requires=['beautifulsoup4']
)