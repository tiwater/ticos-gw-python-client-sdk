#      Copyright 2020. Ticos
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#
#

from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

VERSION = "1.4"

setup(
    version=VERSION,
    name="ticos-mqtt-client",
    author="Ticos",
    author_email="info@ticos.io",
    license="Apache Software License (Apache Software License 2.0)",
    description="Ticos python client SDK",
    url="https://github.com/tiwater/ticos-gw-python-client-sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=["."],
    install_requires=['paho-mqtt>=1.6', 'requests', 'mmh3', 'simplejson'],
    download_url='https://github.com/tiwater/ticos-gw-python-client-sdk/archive/%s.tar.gz' % VERSION)
