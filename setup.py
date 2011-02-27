import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-meio-easytags",
    version = "0.3",
    url = "http://www.meiocodigo.com/projects/django-meio-easytags/",
    license = "BSD",
    description = "An easy way to create custom template tags for Django's templating system.",
    long_description = read('README'),
    author = "Vinicius Mendes",
    author_email = "vbmendes@gmail.com",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires= ['setuptools'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

