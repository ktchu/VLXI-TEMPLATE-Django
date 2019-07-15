"""
Utility functions to support data model and REST API testing.

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
from collections.abc import Sequence

# Django
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.reverse_related import OneToOneRel
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields.reverse_related import ManyToManyRel

# --- Constants

_BASE_UNVERIFIED_FIELDS = ('id', 'created_at', 'modified_at')
_REVERSE_RELATION_FIELD_TYPES = (
    OneToOneRel,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
)


# --- Testing Utility Functions

def verify_obj(obj, expected, skip=None):
    """
    Verify field values for specified object.

    Parameters
    ----------
    obj: Django Model object
        data object to verify

    expected: dict
        expected values for all fields in 'obj'

    skip: Sequence
        list containing names of fields to skip verification for

    Notes
    -----
    * Hidden fields are skipped.
    * Skipped non-hidden fields: defined in _BASE_UNVERIFIED_FIELDS
    """
    # --- Check arguments

    if skip is None:
        skip = []

    else:
        if not isinstance(skip, Sequence):
            raise ValueError("'skip' should be a Sequence")

        elif isinstance(skip, str):
            skip = [skip]

    # --- Preparations

    fields = obj._meta.get_fields()  # pylint: disable=protected-access

    # --- Construct list of fields to skip

    skip.extend(_BASE_UNVERIFIED_FIELDS)

    # Skip reverse relation fields
    for field in fields:
        if isinstance(field, _REVERSE_RELATION_FIELD_TYPES):
            skip.append(field.name)

    # --- Verify field values

    for field in fields:
        if field.name in skip:
            continue

        value = getattr(obj, field.name)
        expected_value = expected[field.name]

        try:
            assert value == expected_value
        except AssertionError:
            message = "obj.{}: assert ".format(field.name)

            if isinstance(value, str):
                message += "'{}' == ".format(value)
            else:
                message += "{} == ".format(value)

            if isinstance(expected_value, str):
                message += "'{}'".format(expected_value)
            else:
                message += "{}".format(expected_value)

            raise AssertionError(message)


def verify_REST_API_item_response(response):  # pylint: disable=invalid-name
    """
    Check common properties of response data for individual items/resources.

    Parameters
    ----------
    response : Response
      Response object returned by APIClient

    Return values
    -------------
    None
    """
    assert 'id' in response.data
    assert 'created_at' not in response.data
    assert 'modified_at' not in response.data
