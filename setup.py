from setuptools import setup, find_packages


setup_args = dict(
    name="callpyback",
    packages=find_packages(),
    version="v0.0.5",  # Ideally should be same as your GitHub release tag varsion
    description="Simple and readable Pure Python callbacks!",
    author="samuelgregorovic",
    author_email="samuelgregorovic@gmail.com",
    url="https://github.com/samuelgregorovic/callpyback",
    download_url="https://github.com/samuelgregorovic/callpyback/archive/refs/tags/v.0.0.5.tar.gz",
    keywords=["callpyback", "callback", "python", "pure", "pythonic"],
    classifiers=[],
)

install_requires = []

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
