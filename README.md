SeleSame
========

Description
-----------

Detection of similar clickable elements on a webpage

Installation
------------

### Simple

    python setup.py install

### Using eggs

    python setup.py bdist_egg
    cd dist
    easy_install <package_name>

Getting started
---------------

Create webdriver of selenium of your browser and pass it with url to get duplicated links on a web page.

    driver = webdriver.Chrome()

    selesame.analyze(
        url = "http://www.xitro.eu",
        driver = driver
    )

For more examples look USAGE file.

Authors
-------

See AUTHORS file.

License
-------

SeleSame is released under The MIT License. See LICENSE file.
