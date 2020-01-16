from setuptools import setup, find_packages
import os.path

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.rst")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")


setup(
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="redash-iodide",
    use_scm_version={"version_scheme": "post-release", "local_scheme": "dirty-tag"},
    setup_requires=["setuptools_scm"],
    description="Extensions to Redash for Iodide by Mozilla",
    project_urls={"homepage": "https://github.com/iodide-project/redash-iodide"},
    author="Mozilla Foundation",
    author_email="dev-webdev@lists.mozilla.org",
    license="MPL-2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment :: Mozilla",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
    entry_points={
        "redash.extensions": [
            "iodide_explore = redash_iodide.explore.extension:extension",
            "iodide_settings = redash_iodide.settings:extension",
        ],
        "redash.bundles": ["iodide_explore = redash_iodide.explore",],
        "redash.periodic_tasks": [],
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["requests", "six",],
    extras_require={
        "test": [
            "flake8==3.5.0",
            "mock",
            "pytest",
            "pytest-cov",
            "pytest-flake8<1.0.1",
        ],
        "dev": ["watchdog"],
    },
)
