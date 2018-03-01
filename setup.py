from setuptools import setup


tests_require = [
    'lektor',
    'pytest',
    'pytest-cov',
    'pytest-mock',
]

setup(
    name='lektor-webpack-support',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    url='http://github.com/lektor/lektor-webpack-support',
    version='0.4',
    license='BSD',
    description='Adds support for webpack to Lektor',
    py_modules=['lektor_webpack_support'],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points={
        'lektor.plugins': [
            'webpack-support = lektor_webpack_support:WebpackSupportPlugin',
        ]
    }
)
