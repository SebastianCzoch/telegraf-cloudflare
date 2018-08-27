import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


setuptools.setup(
    name='telegraf-cloudflare',
    description='Plugin for Telegraf for gathering statistics from Cloudflare',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2.2',
    url='https://github.com/SebastianCzoch/telegraf-cloudflare',
    author='Sebastian Czoch',
    author_email='sebastian@czoch.pl',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    install_requires=read_file('requirements.txt').splitlines(),
    scripts=['telegraf-cloudflare'],
    setup_requires=[
        "flake8"
    ]
    )
