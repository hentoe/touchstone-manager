from http import HTTPStatus

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from touchstone_manager.aero.tests.factories import MaterialFactory
from touchstone_manager.aero.views import material_list_view
from touchstone_manager.users.models import User
from touchstone_manager.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestMaterialListView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        total_material_num = 10
        MaterialFactory.create_batch(total_material_num)
        url = reverse("aero:materials")
        request = rf.get(url)
        request.user = user
        response = material_list_view(request)

        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == total_material_num

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        url = reverse("aero:materials")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = material_list_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestMaterialDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        material = MaterialFactory.create()
        url = reverse("aero:material-detail")
        request = rf.get(url)
        request.user = UserFactory()
        response = material_list_view(request, pk=material.pk)

        assert response.status == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        material = MaterialFactory.create()
        url = reverse("aero:material-detail")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = material_list_view(request, pk=material.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"