from setuptools import setup, find_packages
setup(
        name="hb_pac_disNet",
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        packages=find_packages(exclude=["^\."]),
        exclude_package_data={'': ["Readme.md", "tests"]},
        install_requires=["numpy>=1.11.2",
                          "matplotlib>=1.5.3",
                          "seaborn>=0.7.1",
                          "neo>=0.5.0",
                          "nixio>=1.3",
                          "brian2>=2.0.1",
                          "ipython>=6.1"],
        python_requires=">=3.5",
    )