from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from touchstone_manager.aero.tests.factories import MaterialFactory
from touchstone_manager.aero.tests.factories import MaterialSampleFactory
from touchstone_manager.aero.tests.factories import MeasurementFactory
from touchstone_manager.aero.views import material_detail_view
from touchstone_manager.aero.views import material_list_view
from touchstone_manager.aero.views import material_sample_detail_view
from touchstone_manager.aero.views import material_sample_list_view
from touchstone_manager.aero.views import measurement_detail_view
from touchstone_manager.aero.views import measurement_list_view
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
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = material_list_view(request, pk=material.pk)

        assert response.status_code == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        material = MaterialFactory.create()
        url = reverse("aero:material-detail", kwargs={"pk": material.pk})
        request = rf.get(url)
        request.user = AnonymousUser()
        response = material_detail_view(request, pk=material.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestMaterialSampleListView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        total_material_num = 10
        MaterialSampleFactory.create_batch(total_material_num)
        url = reverse("aero:samples")
        request = rf.get(url)
        request.user = user
        response = material_sample_list_view(request)

        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == total_material_num

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        url = reverse("aero:samples")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = material_sample_list_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestMaterialSampleDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        material = MaterialSampleFactory.create()
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = material_list_view(request, pk=material.pk)

        assert response.status_code == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        material = MaterialSampleFactory.create()
        url = reverse("aero:sample-detail", kwargs={"pk": material.pk})
        request = rf.get(url)
        request.user = AnonymousUser()
        response = material_sample_detail_view(request, pk=material.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestMeasurementListView:
    def test_authenticated(self, user: User, rf: RequestFactory, mocker):
        mocker.patch(
            "touchstone_manager.aero.models.Measurement.process_file",
            return_value=None,
        )
        total_object_num = 10
        MeasurementFactory.create_batch(total_object_num)
        url = reverse("aero:measurements")
        request = rf.get(url)
        request.user = user
        response = measurement_list_view(request)

        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == total_object_num

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        url = reverse("aero:measurements")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = measurement_list_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestMeasurementDetailView:
    @patch("touchstone_manager.aero.models.Measurement.process_file")
    def test_authenticated(self, user: User, rf: RequestFactory, mocker):
        mocker.patch(
            "touchstone_manager.aero.models.Measurement.process_file",
            return_value=None,
        )
        measurement = MeasurementFactory.create()
        url = reverse("aero:measurement-detail", kwargs={"pk": measurement.pk})
        request = rf.get(url)
        request.user = user
        response = measurement_detail_view(request, pk=measurement.pk)

        assert response.status_code == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory, mocker):
        mocker.patch(
            "touchstone_manager.aero.models.Measurement.process_file",
            return_value=None,
        )
        measurement = MeasurementFactory.create()
        url = reverse("aero:measurement-detail", kwargs={"pk": measurement.pk})
        request = rf.get(url)
        request.user = AnonymousUser()
        response = measurement_detail_view(request, pk=measurement.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


class TestHomeViewTemplates(TestCase):
    """Test HomeView uses different templates for authenticated and anonymous users."""

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("home")

    def test_home_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_landing_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "pages/landing.html")
