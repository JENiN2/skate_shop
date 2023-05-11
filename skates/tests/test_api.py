from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from skates.serializers import SkateSerializer
from skates.models import Skate


class SkatesApiTestCase(APITestCase):
    def test_get_list(self):
        skate_1 = Skate.objects.create(name='Trip Out', price=11990, article_number=5361324)
        skate_2 = Skate.objects.create(name='DAILY78 SKTC KVJ0', price=9490, article_number=7362321)

        response = self.client.get(reverse('skates_api_list'))

        serial_data = SkateSerializer([skate_1, skate_2], many=True).data
        serial_data = {'skate_list': serial_data}
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)
