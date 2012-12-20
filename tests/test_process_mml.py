#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import json
import os
import unittest

from testy.assertions import assert_equal, assert_raises

from projectmill.utils import process_mml


class ProcessMMLTestCase(unittest.TestCase):
    def setUp(self):
        self.source = os.path.join(
            os.path.dirname(__file__),
            'data',
            'config_test.json',
        )

    def test_noop_merge(self):
        """Test merging a config with an empty 'mml' attribute."""
        updates = dict(mml=dict())

        with open(self.source) as f:
            source_data = json.loads(f.read())

        result = process_mml(self.source, updates)

        assert_equal(json.loads(result), source_data)

    def test_bad_merge(self):
        """Test merging a config with no 'mml' attribute."""
        with assert_raises(AssertionError):
            process_mml(self.source, dict())


if __name__ == "__main__":
    unittest.main()
