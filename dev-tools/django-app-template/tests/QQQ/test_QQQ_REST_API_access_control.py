"""
REST API access control unit tests for QQQ data model

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject to
the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# --- Imports

# Django
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Local packages
from ..utils import verify_REST_API_item_response


# --- Test Suite

class test_QQQ_REST_API_access_control(  # pylint: disable=invalid-name
        APITestCase):
    """
    REST API access control unit tests for QQQ data model
    """
    # --- Preparation and clean up

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database before running any tests to populate it with
        data records required by tests.

        Notes
        -----
        * setUpTestData() is only called once for the entire TestCase,
          so these database records should not be modified within tests.
        """
        # --- Generate test data

        cls.test_data = {}

        # --- Construct request data for create and edit operations

        cls.request_data = {}

        # --- Get test user

        user_model = get_user_model()
        cls.user = user_model.objects.filter(...)[0]

    def setUp(self):
        """
        Perform preparations required by most tests.
        """
        # --- Authenticate APIClient with test user

        login_succeeded = self.client.login(email=self.user.email,
                                            password='password')
        assert login_succeeded

    def tearDown(self):
        """
        Clean up after each test.
        """
        # --- Log out APIClient

        self.client.logout()

    # --- Tests

    # ------ 'GET' requests

    def test_GET_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'GET' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        verify_REST_API_item_response(response)

    def test_GET_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'GET' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Compute expected number of records
        expected_num_records = ...

        # --- Exercise functionality and check results

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_num_records

    # ------ 'OPTIONS' requests

    def test_OPTIONS_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'OPTIONS' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.options(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

    def test_OPTIONS_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'OPTIONS' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.options(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

    # ------ 'HEAD' requests

    def test_HEAD_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'HEAD' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.head(url)
        assert response.status_code == status.HTTP_200_OK

    def test_HEAD_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'HEAD' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.head(url)
        assert response.status_code == status.HTTP_200_OK

    # ------ 'POST' requests

    def test_POST_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'POST' requests to 'detail' endpoint.

        Notes
        -----
        * Django REST Framework disallows POST requests to 'detail' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.post(url, self.request_data)
        assert response.status_code in expected_status_codes

    def test_POST_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'POST' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.post(url, self.request_data)
        assert response.status_code == status.HTTP_201_CREATED

    # ------ 'PUT' requests

    def test_PUT_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PUT' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.put(url, self.request_data)
        assert response.status_code == status.HTTP_200_OK

    def test_PUT_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PUT' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PUT requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.put(url, self.request_data)
        assert response.status_code in expected_status_codes

    # ------ 'PATCH' requests

    def test_PATCH_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PATCH' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.patch(url, self.request_data)
        assert response.status_code == status.HTTP_200_OK

    def test_PATCH_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PATCH' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PATCH requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.patch(url, self.request_data)
        assert response.status_code in expected_status_codes

    # ------ 'DELETE' requests

    def test_DELETE_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'DELETE' requests to 'detail' endpoint.
        """
        # --- Preparations

        # Create record to use to test DELETE request.
        ...

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_DELETE_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'DELETE' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows DELETE requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API URL
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.delete(url)
        assert response.status_code in expected_status_codes
