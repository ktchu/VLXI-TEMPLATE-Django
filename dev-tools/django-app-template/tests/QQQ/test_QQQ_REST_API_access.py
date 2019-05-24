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

# Standard library
import copy

# Django
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Local packages
from ..utils import verify_REST_API_item_response


# --- Test Suite

class test_QQQ_REST_API_access(APITestCase):
    """
    REST API access control unit tests for QQQ data model
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
        cls.user = user_model.objects.filter(...)[0]

        # --- Construct request data for create and edit operations

        cls.request_data = {}

        # --- Get data objects for detail requests

        # Object that user has access privileges for
        cls.obj_user_has_access = QQQ.objects.filter(...)[0]

        # Object that user does not have access privileges for
        cls.obj_no_user_access = QQQ.objects.filter(...)[0]

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
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.get(url_user_has_access)
        assert response.status_code == status.HTTP_200_OK
        verify_REST_API_item_response(response)

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.get(url_no_user_access)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_GET_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'GET' requests to 'list' endpoint.
        """
        # --- Preparations

        # Compute expected number of records
        expected_num_records = ...

        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_num_records

    # ------ 'OPTIONS' requests

    def test_OPTIONS_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'OPTIONS' requests to 'detail' endpoint.

        Notes
        -----
        * The REST API response data only includes 'actions' when the user
          has permissions and access privileges for the requested item.

        * By default, Django REST Framework only provides 'actions' when
          the user is allowed to make item-level 'PUT' requests.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.options(url_user_has_access)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.options(url_no_user_access)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' not in response.data

    def test_OPTIONS_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'OPTIONS' requests to 'list' endpoint.

        Notes
        -----
        * By default, Django REST Framework only provides 'actions' when
          the user is allowed to make collection-level 'POST' requests.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.options(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'actions' in response.data

    # ------ 'HEAD' requests

    def test_HEAD_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'HEAD' requests to 'detail' endpoint.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.head(url_user_has_access)
        assert response.status_code == status.HTTP_200_OK

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.head(url_no_user_access)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_HEAD_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'HEAD' requests to 'list' endpoint.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.head(url)
        assert response.status_code == status.HTTP_200_OK

    # ------ 'POST' requests

    def test_POST_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'POST' requests to 'detail' endpoint.

        Notes
        -----
        * Django REST Framework disallows POST requests to 'detail' endpoint.

        * Django REST Framework checks permissions before checking whether
          the HTTP method is allowed, so the status code 403 (Forbidden) is
          returned instead of the status code 405 (Method Not Allowed) when
          the user does not have permissions to access the requested record.

        * For POST requests to the 'detail' endpoint, Django REST Framework
          only checks global permissions - it does not check object-level
          permissions.

        * The Django REST Framework DjangoModelPermission class only allows
          POST requests for users with the 'add_modelname' permission for
          the requested data model.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.post(url_user_has_access,
                                    data=self.request_data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.post(url_no_user_access,
                                    data=self.request_data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_POST_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'POST' requests to 'list' endpoint.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.post(url, data=self.request_data)
        assert response.status_code == status.HTTP_201_CREATED

    # ------ 'PUT' requests

    def test_PUT_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PUT' requests to 'detail' endpoint.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.put(url_user_has_access,
                                   data=self.request_data)
        assert response.status_code == status.HTTP_200_OK

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.put(url_no_user_access,
                                   data=self.request_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_PUT_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PUT' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PUT requests to 'list' endpoint.

        * Django REST Framework checks permissions before checking whether
          the HTTP method is allowed, so the status code 403 (Forbidden) is
          returned instead of the status code 405 (Method Not Allowed) when
          the user does not have permissions to access the requested record.

        * The Django REST Framework DjangoModelPermission class only allows
          PUT requests for users with the 'change_modelname' permission for the
          requested object.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.put(url, self.request_data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # ------ 'PATCH' requests

    def test_PATCH_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PATCH' requests to 'detail' endpoint.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(self.obj_user_has_access.pk,))
        response = self.client.patch(url_user_has_access,
                                     data=self.request_data)
        assert response.status_code == status.HTTP_200_OK

        # ------ Object that user does not have access privileges for

        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(self.obj_no_user_access.pk,))
        response = self.client.patch(url_no_user_access,
                                     data=self.request_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_PATCH_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'PATCH' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows PATCH requests to 'list' endpoint.

        * Django REST Framework checks permissions before checking whether
          the HTTP method is allowed, so the status code 403 (Forbidden) is
          returned instead of the status code 405 (Method Not Allowed) when
          the user does not have permissions to access the requested record.

        * The Django REST Framework DjangoModelPermission class only allows
          PATCH requests for users with the 'change_modelname' permission for
          the requested object.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.patch(url, self.request_data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # ------ 'DELETE' requests

    def test_DELETE_detail_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'DELETE' requests to 'detail' endpoint.
        """
        # --- Exercise functionality and check results

        # ------ Object that user has access privileges for

        # Create record to use to test DELETE request.
        obj_user_has_access = QQQ.objects.create(...)

        # Send request and check response
        url_user_has_access = reverse('APP_LABEL:ENDPOINT-detail',
                                      args=(obj_user_has_access.pk,))
        response = self.client.delete(url_user_has_access)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # ------ Object that user does not have access privileges for

        # Create record to use to test DELETE request.
        obj_no_user_access = QQQ.objects.create(...)

        # Send request and check response
        url_no_user_access = reverse('APP_LABEL:ENDPOINT-detail',
                                     args=(obj_no_user_access.pk,))
        response = self.client.delete(url_no_user_access)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_DELETE_list_endpoint(self):  # pylint: disable=invalid-name
        """
        Test access control for 'DELETE' requests to 'list' endpoint.

        Notes
        -----
        * Django REST Framework disallows DELETE requests to 'list' endpoint.

        * Django REST Framework checks permissions before checking whether
          the HTTP method is allowed, so the status code 403 (Forbidden) is
          returned instead of the status code 405 (Method Not Allowed) when
          the user does not have permissions to access the requested record.

        * The Django REST Framework DjangoModelPermission class only allows
          DELETE requests for users with the 'delete_modelname' permission for
          the requested object.
        """
        # --- Exercise functionality and check results

        url = reverse('APP_LABEL:ENDPOINT-list')
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
