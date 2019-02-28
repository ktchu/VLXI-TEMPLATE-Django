"""
Unit tests for 'XYZ' data model

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
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase

# Local packages


# --- Test Suites

class test_XYZ(TestCase):  # pylint: disable=invalid-name
    """
    Unit tests for 'XYZ' data model
    """
    # --- setUp/tearDown

    @classmethod
    def setUpTestData(cls):  # pylint: disable=invalid-name
        """
        Create initial data used by all tests.
        """

    # --- Data model and database tests

    @staticmethod
    def test_BREAD_required_fields_only():  # pylint: disable=invalid-name
        """
        Test basic BREAD operations. Required fields only.
        """
        # pylint: disable=no-member

        # --- Preparations

        # --- Exercise functionality and check results

        # ------ Add

        # Create and verify object

        # ----- Read

        # Retrieve and verify object from database

        # ----- Browse

        # Add additional objects for browse test

        # Verify database contents (e.g., record counts)

        # ------ Edit

        # Edit field values and save object

        # Verify that object with original field values is
        # no longer present in database

        with pytest.raises(ObjectDoesNotExist) as exception_info:
            XYZ.objects.get()
        assert 'XYZ matching query does not exist' in str(exception_info)

        # Retrieve and verify object from database

        # ------ Delete

        # Delete object
        pk = obj_from_db.id  # pylint: disable=invalid-name
        obj_from_db.delete()

        # Verify that object is no longer present in database
        with pytest.raises(ObjectDoesNotExist) as exception_info:
            XYZ.objects.get(pk=pk)
        assert 'XYZ matching query does not exist' in str(exception_info)

    @staticmethod
    def test_BREAD_with_optional_fields():  # pylint: disable=invalid-name
        """
        Test basic BREAD operations. Optional fields included.
        """
        # pylint: disable=no-member

        # --- Preparations

        # --- Exercise functionality and check results

        # ------ Add

        # Create and verify object

        # ----- Read

        # Retrieve and verify object from database

        # ----- Browse

        # Add additional objects for browse test

        # Verify database contents (e.g., record counts)

        # ------ Edit

        # Edit field values and save object

        # Verify that object with original field values is
        # no longer present in database

        with pytest.raises(ObjectDoesNotExist) as exception_info:
            XYZ.objects.get()
        assert 'XYZ matching query does not exist' in str(exception_info)

        # Retrieve and verify object from database

        # ------ Delete

        # Delete object
        pk = obj_from_db.id  # pylint: disable=invalid-name
        obj_from_db.delete()

        # Verify that object is no longer present in database
        with pytest.raises(ObjectDoesNotExist) as exception_info:
            XYZ.objects.get(pk=pk)
        assert 'XYZ matching query does not exist' in str(exception_info)

    @staticmethod
    def test_not_null_constraints():
        """
        Test NOT NULL constraints.

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
                XYZ.objects.create()

        assert 'NOT NULL constraint failed: ' \
               'xyz.abc_id' in str(exception_info)

    @staticmethod
    def test_unique_constraints():
        """
        Test unique constraints.
        """
        # --- Preparations

        # Create object

        # --- Exercise functionality and check results

        # Attempt to create duplicate object
        with pytest.raises(IntegrityError) as exception_info:
            with transaction.atomic():
                XYZ.objects.create()

        assert 'UNIQUE constraint failed' in str(exception_info)
        assert 'xyz.field_1' in str(exception_info)
        assert 'xyz.field_2' in str(exception_info)

    @staticmethod
    def test_integrity_constraints():
        """
        Test other integrity constraints.
        """

    @staticmethod
    def test_validated_fields():
        """
        Test validated fields.
        """
        # --- 'field_1'

        # Preparations

        # Create object

        # Validate object
        with pytest.raises(ValidationError) as exception_info:
            obj.full_clean()
        assert "'field_1': ['Error message.'" in str(exception_info)

    @staticmethod
    def test_many_to_one_relationships():
        """
        Test many-to-one relationships.

        Notes
        -----
        * Many-to-one relationships should be tested from the data model that
          containing the ForeignKey field.
        """
        # --- 'field_1'

        # Create object

        # Verify forward relationship

        # Verify reverse relationship

    @staticmethod
    def test_many_to_many_relationships():
        """
        Test many-to-many relationships.

        Notes
        -----
        * Many-to-many relationships should be tested from the data model that
          containing the ManyToManyField.
        """
        # --- 'field_1'

        # Create object

        # Verify forward relationship

        # Verify reverse relationship

    @staticmethod
    def test_one_to_one_relationships():
        """
        Test one-to-one relationships.

        Notes
        -----
        * One-to-one relationships should be tested from the data model that
          containing the OneToOneField.
        """
        # --- 'field_1'

        # Create object

        # Verify forward relationship

        # Verify reverse relationship

    # --- Property and method tests

    @staticmethod
    def test_properties():
        """
        Test properties.
        """

    # --- Other tests (e.g., signals, custom permissions, etc.)
