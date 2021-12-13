import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Social-media-notifier",
    version="0.0.1",
    author="Simon Theilgård Maribo",
    author_email="maribo@mensa.dk",
    description="Package to receive notifications from various social media platforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Simonmaribo/Social-Media-Notifier",
    project_urls={
        "Bug Tracker": "https://github.com/Simonmaribo/Social-Media-Notifier/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)