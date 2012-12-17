#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import copy

from testify import (
    TestCase, setup, teardown, assert_equal, assert_raises, run
)

from projectmill.utils import merge_config


class DictMergeTestCase(TestCase):
    @setup
    def create_src(self):
        self.merge_left = dict(
            a=1,
            b=2,
            c=dict(
                c1='a',
                c2='b',
            )
        )

    def test_mutation(self):
        """Make sure `merge_left` and `merge_right` are unmodified."""
        merge_right = dict(
            a=1,
            b=dict(b1=3),
        )

        orig_left = copy.deepcopy(self.merge_left)
        orig_right = copy.deepcopy(merge_right)

        merge_config(self.merge_left, merge_right)

        assert_equal(self.merge_left, orig_left)
        assert_equal(merge_right, orig_right)

    def test_missing_right(self):
        """Missing keys in `merge_right` are ignored."""
        merge_right = dict(
            a=1,
            b=dict(b1=3),
        )
        result = merge_config(self.merge_left, merge_right)

        assert_equal(result, dict(
            a=1,
            b=dict(b1=3),
            c=dict(
                c1='a',
                c2='b',
            )
        ))

    def test_nested_merge(self):
        """Make sure it's not only top-level keys being merged."""
        merge_right = dict(
            a=1,
            b=2,
            c=dict(
                c1='a',
                c2='c',
            )
        )
        result = merge_config(self.merge_left, merge_right)

        assert_equal(result, dict(
            a=1,
            b=2,
            c=dict(
                c1='a',
                c2='c',
            )
        ))

    def test_null_merge(self):
        """Merging a dict with None"""
        result = merge_config(self.merge_left, None)
        assert_equal(result, None)

    def test_bad_merge(self):
        """Merge non-dicts"""
        result = None
        with assert_raises(TypeError):
            result = merge_config(4, dict(a=1))

        assert_equal(result, None)

    def test_bad_left(self):
        """Merge dict into non-dict"""
        result = None
        with assert_raises(TypeError):
            result = merge_config(4, dict(a=1))

        assert_equal(result, None)

    def test_noop_merge(self):
        """Merging a dict with itself"""
        result = merge_config(self.merge_left, self.merge_left)
        assert_equal(result, self.merge_left)

    @teardown
    def clear_src(self):
        self.src = dict()


if __name__ == "__main__":
    run()
