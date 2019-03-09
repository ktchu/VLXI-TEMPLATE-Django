"""
Utility functions to support testing.

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


# --- Constants

_BASE_UNVERIFIED_FIELDS = ['id', 'created_at', 'modified_at']


# --- Test Suites

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
    # Check arguments
    if skip is None:
        skip = []

    else:
        if not isinstance(skip, Sequence):
            raise ValueError("'skip' should be a Sequence")

        if isinstance(skip, str):
            skip = [skip]

    # Construct list of fields to skip
    skip.extend(_BASE_UNVERIFIED_FIELDS)

    # Get (non-hidden) fields
    fields = obj._meta.get_fields()  # pylint: disable=protected-access

    # Verify field values
    for field in fields:
        if field.name in skip:
            continue

        assert getattr(obj, field.name) == expected[field.name]
