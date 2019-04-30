"""
Unit tests for QQQ data model

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject to
the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# --- Imports

# Standard library
import copy

# pytest
import pytest

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase

# Local packages
from ..utils import verify_obj


# --- Test Suite

class test_QQQ(TestCase):  # pylint: disable=invalid-name
    """
    Unit tests for QQQ data model
    """
    # --- Test preparation and clean up

    @classmethod
    def setUpTestData(cls):  # pylint: disable=invalid-name
        """
        Initialize database before running any tests to populate it with
        data records required by tests.

        Notes
        -----
        * setUpTestData() is only called once for the entire TestCase,
          so these database records should not be modified within tests.
        """

    def setUp(self):  # pylint: disable=invalid-name
        """
        Perform preparations required by most tests.

        - Construct test record to use when creating data objects.
        """
        # --- Test record to use when creating data objects

        self.test_record = {}

    def tearDown(self):  # pylint: disable=invalid-name
        """
        Clean up after each test.
        """

    # --- Tests

    def test_BREAD(self):  # pylint: disable=invalid-name
        """
        Test basic BREAD operations.

        - The 'add' operation is tested with required fields only.
        """
        # pylint: disable=no-member

        # --- Exercise functionality and check results

        # ------ Add

        # Create and verify object
        obj = QQQ.objects.create()

        expected_record = copy.deepcopy(self.test_record)
        verify_obj(obj, expected_record)

        # ----- Read

        # Retrieve and verify object from database
        obj_from_db = QQQ.objects.get(pk=obj.pk)

        # ----- Browse

        # Add additional objects for browse test

        # Verify database contents (e.g., record counts)

        # ------ Edit

        # Edit field values and save object

        # Verify that object with original field values is
        # no longer present in database

        with pytest.raises(ObjectDoesNotExist) as exception_info:
            QQQ.objects.get()
        assert 'QQQ matching query does not exist' in str(exception_info)

        # Retrieve and verify object from database
        obj_from_db = QQQ.objects.get(pk=obj_from_db.pk)

        # ------ Delete

        # Delete object
        pk = obj_from_db.pk   # pylint: disable=invalid-name
        obj_from_db.delete()

        # Verify that object is no longer present in database
        with pytest.raises(ObjectDoesNotExist) as exception_info:
            QQQ.objects.get(pk=pk)
        assert 'QQQ matching query does not exist' in str(exception_info)

    def test_add_optional_fields(self):
        """
        Test 'add' operation with optional fields included.
        """
        # pylint: disable=no-member

        # --- Exercise functionality and check results

        # ------ Add

        # Create and verify object
        obj = QQQ.objects.create()

        # ----- Read

        # Retrieve and verify object from database
        obj_from_db = QQQ.objects.get(pk=obj.pk)

    def test_add_not_null_constraints(self):
        """
        Test NOT NULL constraints when adding objects.

        Notes
        -----
        * When CharField values are set to None, they are stored in the
          database as an empty string. As a result, no error is raised
          when CharField values are not set when creating a new model object.
        """
        # --- Exercise functionality and check results

        # ------ Missing 'abc' field

        with pytest.raises(IntegrityError) as exception_info:
            with transaction.atomic():
                QQQ.objects.create()

        assert 'NOT NULL constraint failed: ' \
               'xyz.abc_id' in str(exception_info)

    def test_add_unique_constraints(self):
        """
        Test uniqueness constraints when adding objects.
        """
        # --- Exercise functionality and check results

        # Create object

        # Attempt to create duplicate object
        with pytest.raises(IntegrityError) as exception_info:
            with transaction.atomic():
                QQQ.objects.create()

        assert 'UNIQUE constraint failed' in str(exception_info)
        assert 'xyz.field_1' in str(exception_info)
        assert 'xyz.field_2' in str(exception_info)

    def test_validated_fields(self):
        """
        Test validated fields.

        Notes
        -----
        * To test field validation, do _not_ use `Model.objects.create()` to
          create the object because some fields get modified during the
          process and the validation error may not be caught. Create an object
          directly and use ```full_clean()``` method to check for invalid
          fields.
        """
        # --- 'field_1'

        # Create object with invalid field value

        # Validate object
        with pytest.raises(ValidationError) as exception_info:
            obj.full_clean()
        assert "'field_1': ['Error message.'" in str(exception_info)

    def test_many_to_one_relationships(self):
        """
        Test many-to-one relationships.

        Notes
        -----
        * Many-to-one relationships should be tested from the data model that
          containing the ForeignKey field.
        """
        # Create object

        # Verify forward and reverse relationships

        # Verify 'on_delete' behavior

    def test_many_to_many_relationships(self):
        """
        Test many-to-many relationships.

        Notes
        -----
        * Many-to-many relationships should be tested from the data model that
          containing the ManyToManyField.
        """
        # Create object

        # Verify forward and reverse relationships

        # Verify 'on_delete' behavior

    def test_one_to_one_relationships(self):
        """
        Test one-to-one relationships.

        Notes
        -----
        * One-to-one relationships should be tested from the data model that
          containing the OneToOneField.
        """
        # Create object

        # Verify forward and reverse relationships

        # Verify 'on_delete' behavior

    # --- Property and method tests

    def test_properties(self):
        """
        Test properties.
        """

    # --- Other tests (e.g., signals, custom permissions, etc.)
