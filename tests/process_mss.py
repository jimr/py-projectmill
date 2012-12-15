#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import json
import os

from testify import (
    TestCase, setup, assert_equal, assert_not_equal, assert_match_regex, run
)

from projectmill.utils import process_mss, MSS_VAR_RE


class ProcessMSSTestCase(TestCase):
    @setup
    def read_source(self):
        base_path = os.path.join(
            os.path.dirname(__file__),
            'data',
        )

        with open(os.path.join(base_path, 'config_test.json')) as f:
            self.config = json.loads(f.read())

        self.source = os.path.join(base_path, 'style.mss')

    def test_simple_merge(self):
        """Test merging a config with an empty 'cartoVars' attribute."""
        with open(self.source) as f:
            source_mss = f.read().decode('utf8')

        result = process_mss(self.source, self.config)
        lines = result.splitlines()
        source_lines = source_mss.splitlines()

        # Make sure we changed something, but that the number of lines is
        # unchanged
        assert_not_equal(result, source_mss)
        assert_equal(len(lines), len(source_lines))

        for i, (old, new) in enumerate(zip(source_lines, lines)):
            # We know there's a variable on this line that has a substitution
            # in our test config
            if i == 29:
                # Make sure we've changed something, but that the new output is
                # still a valid MSS variable
                assert_not_equal(old, new)
                assert_match_regex(MSS_VAR_RE, new)
                assert_equal(
                    new[-5:-1],
                    self.config.get('cartoVars').get('park')
                )
            else:
                assert_equal(old, new)


if __name__ == "__main__":
    run()
