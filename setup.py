import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GitFx",
    version="0.0.5",
    author="B1nj0y",
    author_email="idegorepl@gmail.com",
    description="Create a Serverless service in Git hosting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitx-io/GitFx",
    project_urls={
        "Bug Tracker": "https://github.com/gitx-io/GitFx/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=["gitfx"],
    python_requires=">=3.6",
)
