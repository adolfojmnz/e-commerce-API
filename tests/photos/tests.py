from django.test import TestCase

from photos.models import WatchPhoto

from tests.watches.tests import SetUpMixin as SetUpWatchMixin

import os


class SetUpMixin(SetUpWatchMixin):

    WATCH_PHOTO_DATA = {
        'main': True,
        'file': os.path.join(
            os.path.abspath('.'), 'tests/photos/photo.jpeg'
        )
    }

    def upload_watch_photo(self, watch):
        self.WATCH_PHOTO_DATA['watch'] = watch
        photo = WatchPhoto.objects.create(**self.WATCH_PHOTO_DATA)
        photo.save()
        return photo


class TestWatchPhoto(SetUpMixin, TestCase):

    def setUp(self):
        vendor = self.create_user()
        collection = self.create_collection(vendor)
        watch = self.create_watch(collection)
        self.watch_photo = self.upload_watch_photo(watch)

    def test_watch_photo(self):
        retrieved_photo = WatchPhoto.objects.get(pk=self.watch_photo.pk)
        self.assertEqual(self.watch_photo.watch, retrieved_photo.watch)
        self.assertEqual(self.watch_photo.main, retrieved_photo.main)
        self.assertEqual(self.watch_photo.file, retrieved_photo.file)

