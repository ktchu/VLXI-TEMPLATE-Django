"""
REST API access control unit tests for 'XYZ' data model

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
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# --- Test Suites

class test_XYZ_REST_API_access_control(  # pylint: disable=invalid-name
        APITestCase):
    """
    REST API access control unit tests for 'XYZ' data model
    """
    # --- Test preparation and clean up

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
        # Generate test data
        cls.test_data = {}

    def setUp(self):
        """
        Perform preparations required by most tests.

        - Construct test record to use when creating data objects.

        - Authenticate APIClient.
        """
        # --- Test record to use when creating data objects

        self.test_record = {}

        # --- Authenticate APIClient (with admin user)

        email = 'admin-1@example.com'
        password = 'admin-1'
        login_succeeded = self.client.login(email=email, password=password)
        assert login_succeeded

    def tearDown(self):
        """
        Clean up after each test.

        - Log out APIClient.
        """
        # --- Log out APIClient

        self.client.logout()

    # --- Test REST API access control

    # ------ 'GET' requests

    def test_get_request_detail_endpoint(self):
        """
        Test access control for 'GET' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        run_basic_item_response_checks(response)

    def test_get_request_list_endpoint(self):
        """
        Test access control for 'GET' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_num_records

    # ------ 'OPTIONS' requests

    def test_options_request_detail_endpoint(self):
        """
        Test access control for 'OPTIONS' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.options(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

    def test_options_request_list_endpoint(self):
        """
        Test access control for 'OPTIONS' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.options(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

    # ------ 'HEAD' requests

    def test_head_request_detail_endpoint(self):
        """
        Test access control for 'HEAD' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.head(url)
        assert response.status_code == status.HTTP_200_OK

    def test_head_request_list_endpoint(self):
        """
        Test access control for 'HEAD' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # --- Exercise functionality and check results

        response = self.client.head(url)
        assert response.status_code == status.HTTP_200_OK

    # ------ 'POST' requests

    def test_post_request_detail_endpoint(self):
        """
        Test access control for 'POST' requests to 'detail' endpoint.

        Notes
        -----
        * Django REST Framework disallows POST requests to 'detail' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # Data for request
        data = {}

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.post(url, data)
        assert response.status_code in expected_status_codes

    def test_post_request_list_endpoint(self):
        """
        Test access control for 'POST' requests to 'list' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Data for request
        data = {}

        # --- Exercise functionality and check results

        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    # ------ 'PUT' requests

    def test_put_request_detail_endpoint(self):
        """
        Test access control for 'PUT' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # Data for request
        data = {}

        # --- Exercise functionality and check results

        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_list_endpoint(self):
        """
        Test access control for 'PUT' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PUT requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Data for request
        data = {}

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.put(url, data)
        assert response.status_code in expected_status_codes

    # ------ 'PATCH' requests

    def test_patch_request_detail_endpoint(self):
        """
        Test access control for 'PATCH' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # Data for request
        data = {}

        # --- Exercise functionality and check results

        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_patch_request_list_endpoint(self):
        """
        Test access control for 'PATCH' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PATCH requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Data for request
        data = {}

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.patch(url, data)
        assert response.status_code in expected_status_codes

    # ------ 'DELETE' requests

    def test_delete_request_detail_endpoint(self):
        """
        Test access control for 'DELETE' requests to 'detail' endpoint.
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-detail', args=(pk,))

        # --- Exercise functionality and check results

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_request_list_endpoint(self):
        """
        Test access control for 'DELETE' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows DELETE requests to 'list' endpoint.

        * Depending on the order that permissions are checked, the HTTP
          response status may be 403 (Forbidden) or 405 (Method Not Allowed).
        """
        # --- Preparations

        # REST API endpoint
        url = reverse('APP_LABEL:ENDPOINT-list')

        # Expected status codes
        expected_status_codes = [status.HTTP_403_FORBIDDEN,
                                 status.HTTP_405_METHOD_NOT_ALLOWED]

        # --- Exercise functionality and check results

        response = self.client.delete(url)
        assert response.status_code in expected_status_codes
