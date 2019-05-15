"""
REST API unit tests for QQQ data model

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
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Local packages
from ..utils import verify_obj
from ..utils import verify_REST_API_item_response


# --- Test Suite

class test_QQQ_REST_API(APITestCase):
    """
    REST API unit tests for QQQ data model
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

        cls.test_data = {}

        # --- Get test user

        user_model = get_user_model()
        cls.user = user_model.objects.filter(is_superuser=True)[0]

    def setUp(self):
        """
        Perform preparations required by most tests.
        """
        # --- Authenticate APIClient with test user

        login_succeeded = self.client.login(email=self.user.email,
                                            password='admin')
        assert login_succeeded

    def tearDown(self):
        """
        Clean up after each test.
        """
        # --- Log out APIClient

        self.client.logout()

    # --- Tests

    def test_list(self):
        """
        Test 'list' function (GET request to 'list' endpoint).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        # Send request
        response = self.client.get(url)

        # Check response
        assert response.status_code == status.HTTP_200_OK

    def test_list_with_filters(self):
        """
        Test 'list' function (GET request to 'list' endpoint) with filters.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        # Construct request data
        data = {}

        # Send request
        response = self.client.get(url, data)

        # Check response
        assert response.status_code == status.HTTP_200_OK

    def test_create(self):
        """
        Test 'create' function (POST request to 'list' endpoint).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        # Construct request data
        data = {}

        # Send request
        response = self.client.post(url, data)

        # Check response
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_with_data_field_violations(self):
        """
        Test 'create' function (POST request to 'list' endpoint) with
        data field violations.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        # ------ Missing required fields

        # List of required fields
        required_fields = []

        # Construct request data
        data = {}

        # Verify that error is raised for each required field
        invalid_data = copy.deepcopy(data)
        for required_field in required_fields:
            del invalid_data[required_field]

        # Send request
        response = self.client.post(url, invalid_data)

        # Check response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        for required_field in required_fields:
            assert required_field in response.data

            error_codes = [error.code for error
                           in response.data[required_field]]
            expected_error_codes = ['required']
            for error_code in expected_error_codes:
                assert error_code in error_codes

            errors = [str(error) for error in response.data[required_field]]
            expected_errors = ['This field is required.']
            for error in expected_errors:
                assert error in errors

    def test_create_with_uniqueness_violations(self):
        """
        Test 'create' function (POST request to 'list' endpoint) with
        uniqueness violations.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        # Construct request data
        data = {}

        # Send request
        response = self.client.post(url, data)

        # Check response
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Example: unique field
        assert 'field' in response.data
        error_codes = [error.code for error in response.data['field']]
        expected_error_codes = ['unique']
        for error_code in expected_error_codes:
            assert error_code in error_codes

        errors = [str(error) for error in response.data['field']]
        expected_errors = ['This field must be unique.']
        for error in expected_errors:
            assert error in errors

        # Example: unique_together
        assert 'non_field_errors' in response.data
        error_codes = [error.code for error
                       in response.data['non_field_errors']]
        expected_error_codes = ['unique']
        for error_code in expected_error_codes:
            assert error_code in error_codes

        errors = [str(error) for error in response.data['non_field_errors']]
        expected_errors = ['The fields xx, yy, zz '
                           'must make a unique set.']
        for error in expected_errors:
            assert error in errors

        # Check database record count

    def test_retrieve(self):
        """
        Test 'retrieve' function (GET request to 'detail' endpoint).
        """
        # --- Preparations

        # pk of object to retrieve
        pk = 1

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        # Send request
        response = self.client.get(url)

        # Check response
        assert response.status_code == status.HTTP_200_OK
        verify_REST_API_item_response(response)

    def test_update(self):
        """
        Test 'update' function (PUT request to 'detail' endpoint).
        """
        # --- Preparations

        # Get object to update
        # obj = ...

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(obj.pk,))

        # --- Exercise functionality and check results

        # ------ 'PUT' request with valid data

        # Construct request data
        data = {}

        # Send request
        response = self.client.put(url, data)

        # Check response
        assert response.status_code == status.HTTP_200_OK

        # ------ Verify that 'PUT' is idempotent

        # ------ 'PUT' request with invalid data

        # Check that request fails

        # Verify that database record has not be updated

    def test_partial_update(self):
        """
        Test 'partial_update' function (PATCH request to 'detail' endpoint).
        """
        # --- Preparations

        # Get object to update
        # obj = ...

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(obj.pk,))

        # --- Exercise functionality and check results

        # ------ 'PATCH' request with valid data

        # Construct request data
        data = {}

        # Send request
        response = self.client.patch(url, data)

        # Check response
        assert response.status_code == status.HTTP_200_OK

        # ------ 'PATCH' request with invalid data

        # Check that request fails

        # Verify that database record has not be updated

    def test_destroy(self):
        """
        Test 'destroy' function (DELETE request to 'detail' endpoint).
        """
        # --- Preparations

        # Get object to destroy
        # obj = ...

        # --- Exercise functionality and check results

        # Delete record
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(obj.pk,))

        # Send request
        response = self.client.delete(url)

        # Check response
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check that 'GET' request returns 404 error
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
