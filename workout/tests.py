from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestPreparations(APITestCase):
    NAME = "Preparation Test"
    DESC = "Preparation Des"
    URL = "/api/v1/workout/preparations"

    def setUp(self):
        models.Preparation.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_preparations(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_preparation(self):
        new_preparation_name = "New Preparation"
        new_description_name = "New Description"

        response = self.client.post(
            self.URL,
            data={
                "name": new_preparation_name,
                "description": new_description_name,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(
            data["name"],
            new_preparation_name,
        )

        self.assertEqual(
            data["description"],
            new_description_name,
        )

        response = self.client.post(self.URL)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestPreparation(APITestCase):
    NAME = "Test Preparation"
    DESC = "Test Description"
    UPDATE_NAME = "Update Amenity"
    UPDATE_DESC = "Update Description"

    def setUp(self):
        models.Preparation.objects.create(name=self.NAME, description=self.DESC)

    def test_get_preparation_not_found(self):
        response = self.client.get("/api/v1/workout/preparations/2")

        self.assertEqual(response.status_code, 404)

    def test_get_preparation(self):
        response = self.client.get("/api/v1/workout/preparations/2")

        self.assertEqual(response.status_code, 404)

        response = self.client.get("/api/v1/workout/preparations/1")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )

        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_preparation(self):
        response = self.client.put(
            "/api/v1/workout/preparations/1",
            data={"name": self.UPDATE_NAME, "description": self.UPDATE_DESC},
        )

        data = response.json()
        self.assertEqual(data["name"], self.UPDATE_NAME)
        self.assertEqual(data["description"], self.UPDATE_DESC)
        self.assertEqual(response.status_code, 200)

        name_len_200 = "a" * 200
        name_validate_response = self.client.put(
            "/api/v1/workout/preparations/1",
            data={"name": name_len_200},
        )
        data = name_validate_response.json()
        self.assertIn("name", data)
        self.assertNotIn("decs", data)
        self.assertEqual(name_validate_response.status_code, 400)

    def test_delete_preparation(self):
        response = self.client.delete("/api/v1/workout/preparations/1")

        self.assertEqual(response.status_code, 204)


class TestWorkouts(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_workout(self):
        response = self.client.post("/api/v1/workout/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )

        response = self.client.post("/api/v1/workout/")
        print(response.json())
