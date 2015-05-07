try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description' : 'My Project',
    'author' : 'Pichugin Viacheslav',
    'url' : 'URL to get it at.',
    'download_url' : 'Where to download it.',
    'author_email' : 'pva33@mail.ru',
    'version' : '0.1',
    'install_requeries' : ['nose'],
    'packages' : ['NAME'],
    'scripts' : [],
    'name' : 'projectname'
}

setup(**config)