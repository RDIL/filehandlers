import setuptools

with open("README.md", mode="r") as FILE_HANDLER:
    LONG_DESCRIPTION = FILE_HANDLER.read()

setuptools.setup(
    name='filehandlers',
    version='2.11.0',
    license="MIT",
    description='Package containing code to help in working with files.',
    packages=setuptools.find_packages(),
    author='Reece Dunham',
    author_email='me@rdil.rocks',
    url='https://github.com/RDIL/filehandlers',
    project_urls={
        'Documentation': 'https://filehandlers.rdil.rocks',
        'Source Code': 'https://github.com/RDIL/filehandlers',
        'Bug Tracker': 'https://github.com/RDIL/filehandlers/issues'
    },
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "file",
        "files",
        "handler",
        "handlers",
        "io"
    ],
    python_requires=">=3.3"
)
