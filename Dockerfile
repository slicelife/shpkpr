FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# tox isn't defined in requirements-test.txt because it needs to be installed
# globally. The dependencies in requirements-test.txt are only used for tests
# and are installed by tox at runtime
RUN pip install --no-cache-dir tox

# pre-install exact dependency versions using pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# install the app with pip (because the dcos dependency blows up when you
# attempt to use `setup.py install`)
COPY . /usr/src/app
RUN pip install .

CMD ["shpkpr"]
