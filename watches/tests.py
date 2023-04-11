from django.test import TestCase

from datetime import datetime

from accounts.tests import CreateUserMixin
from watches.models import Watch, Collection


class SetUpMixin(CreateUserMixin):

    COLLECTION_DATA = {
        'name': 'The Nucleus Collection (42mm)',
        'brand': 'Holzkern',
        'description': 'Test description',
        'release_date': '2023-04-01',
    }

    WATCH_DATA = {
        'model_name': 'Cobalt (Walnut/Blue)',
        'is_waterproof': True,
        'has_date_indicator': False,
        'has_cronograph_features': False,
        'color': 'D',
        'diameter': 42,
        'movement': 'Q',
        'case_material': 'M-W',
        'bracelet_material': 'M-W',
        'release_date': '2023-04-01',
        'description': 'test description',
        'price': 499
    }

    def create_vendor(self):
        user = super().create_user()
        user.save()
        return user

    def create_collection(self, vendor):
        self.COLLECTION_DATA['vendor'] = vendor
        collection = Collection.objects.create(**self.COLLECTION_DATA)
        collection.save()
        return collection

    def create_watch(self, collection):
        self.WATCH_DATA['collection'] = collection
        watch = Watch.objects.create(**self.WATCH_DATA)
        watch.save()
        return watch


class TestWatchModel(SetUpMixin, TestCase):

    def setUp(self):
        self.vendor = self.create_vendor()
        self.collection = self.create_collection(self.vendor)
        self.watch = self.create_watch(self.collection)

    def test_watch(self):
        collection_queryset = Watch.objects.filter(
            collection__name__icontains='Nucleus'
        )
        retrived_watch = collection_queryset.get(
            model_name='Cobalt (Walnut/Blue)'
        )
        self.assertEqual(self.watch.pk, retrived_watch.pk)
        self.assertEqual(self.watch.collection, retrived_watch.collection)
        self.assertEqual(self.watch.model_name, retrived_watch.model_name)
        self.assertEqual(self.watch.is_waterproof,
                         retrived_watch.is_waterproof)
        self.assertEqual(self.watch.has_date_indicator,
            retrived_watch.has_date_indicator
        )
        self.assertEqual(self.watch.has_cronograph_features,
            retrived_watch.has_cronograph_features
        )
        self.assertEqual(self.watch.color, retrived_watch.color)
        self.assertEqual(self.watch.diameter, retrived_watch.diameter)
        self.assertEqual(self.watch.movement, retrived_watch.movement)
        self.assertEqual(self.watch.case_material,
                         retrived_watch.case_material)
        self.assertEqual(self.watch.bracelet_material,
            retrived_watch.bracelet_material
        )
        self.assertEqual(
            datetime.strptime(self.watch.release_date, '%Y-%m-%d').date(),
            retrived_watch.release_date)
        self.assertEqual(self.watch.description, retrived_watch.description)
        self.assertEqual(self.watch.price, retrived_watch.price)
