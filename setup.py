try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'crawl for gsxt',
    'author': 'alan@fxiaoke.com',
    'url': 'http://git.firstshare.cn/fslink/gsxt-crawl',
    'download_url': 'git@git.firstshare.cn:fslink/gsxt-crawl.git',
    'author_email': 'alan@fxiaoke.com',
    'version': '0.1',
    'install_requires': ['nose', 'scrapy'],
    'packages': ['gsxtCrawl'],
    'scripts': [],
    'name': 'gsxt-crawl'
}

setup(**config)