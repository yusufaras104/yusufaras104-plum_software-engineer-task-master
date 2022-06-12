import json
import functools
import os
import sys

import pytest
from flask import Flask

# Set up the path to import from `shorty`.
root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from shorty.app import create_app  # noqa


class TestResponseClass(Flask.response_class):
    @property
    def json(self):
        return json.loads(self.data)
