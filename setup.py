from setuptools import setup, find_packages

setup(
    name = "django-meio-easytags",
    version = "0.1",
    url = "http://github.com/vbmendes/django-meio-easytags",
    license = "BSD",
    description = "An easier way to write template tags for Django's template system.",
    author = "Vinicius Mendes",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires= ['setuptools'],
)

