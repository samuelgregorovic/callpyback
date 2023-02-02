from setuptools import setup, find_packages


setup_args = dict(
    name="callpyback",
    packages=find_packages(),
    version="v1.0.0",
    description="Simple and readable Pure Python callbacks!",
    author="samuelgregorovic",
    author_email="samuelgregorovic@gmail.com",
    url="https://github.com/samuelgregorovic/callpyback",
    download_url="https://github.com/samuelgregorovic/callpyback/archive/refs/tags/v.1.0.0.tar.gz",
    keywords=["callpyback", "callback", "python", "pure", "pythonic"],
    classifiers=[],
)

install_requires = []

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)

# $ python setup.py sdist
# $ twine upload dist/callpyback-v1.0.0.tar.gz
