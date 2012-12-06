from setuptools import setup, find_packages

setup(
        name='cmsplugin_newswithimages',
        version='1.1',
        description='Django cms plugin for insert newss',
        author='Colleoni Luca for fbk',
        author_email='colleoni@fbk.eu',
        packages = find_packages(),
        install_requires = [
                              "Django>=1.4.1",
                              "django-cms",
                              "django-sekizai",
                              "PIL",
                              "easy-thumbnails >= 1.0",
                              "django-filer",    
                            ],
        include_package_data=True,
        zip_safe=False,
)
