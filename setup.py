from setuptools import setup

setup(
    name='lektor-webpack-support',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    url='http://github.com/lektor/lektor-webpack-support',
    version='0.1',
    license='BSD',
    description='Adds support for webpack to Lektor',
    py_modules=['lektor_webpack_support'],
    entry_points={
        'lektor.plugins': [
            'webpack-support = lektor_webpack_support:WebpackSupportPlugin',
        ]
    }
)
