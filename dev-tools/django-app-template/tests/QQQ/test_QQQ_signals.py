"""
Unit tests for signal handlers for QQQ data model

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject to
the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# --- Imports

# pytest
import pytest

# Django
from django.test import TestCase


# --- Test Suite

class test_QQQ_signals(TestCase):
    """
    Unit tests for signal handlers for QQQ data model

    Notes
    -----
    * Each signal handler that receives signals from instances of the data
      model has its own unit test method.
    """
    # --- Preparation and clean up

    @classmethod
    def setUpTestData(cls):
        """
        Generate test data (e.g., database records). Perform preparations
        required by most tests (to redundant operations).

        Notes
        -----
        * setUpTestData() is only called once for the entire TestCase,
          so these database records should not be modified within tests.
        """
        # --- Generate test data

        cls.test_data = generate_test_data()

    def setUp(self):
        """
        Perform preparations required by most tests.
        """

    def tearDown(self):
        """
        Clean up after each test.
        """

    # --- Tests

    def test_post_save(self):  # pylint: disable=invalid-name
        """
        Test handler for 'post_save' signal.
        """
        # pylint: disable=no-member

        # --- Preparations

        # --- Exercise functionality and check results
