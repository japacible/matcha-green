from __future__ import with_statement, absolute_import

from operator import attrgetter

from django.db import connection
from django.test import TestCase, skipIfDBFeature
from django.test.utils import override_settings

from .models import Country, Restaurant, Pizzeria, State, TwoFields


class BulkCreateTests(TestCase):
    def setUp(self):
        self.data = [
            Country(name="United States of America", iso_two_letter="US"),
            Country(name="The Netherlands", iso_two_letter="NL"),
            Country(name="Germany", iso_two_letter="DE"),
            Country(name="Czech Republic", iso_two_letter="CZ")
        ]

    def test_simple(self):
        created = Country.objects.bulk_create(self.data)
        self.assertEqual(len(created), 4)
        self.assertQuerysetEqual(Country.objects.order_by("-name"), [
            "United States of America", "The Netherlands", "Germany", "Czech Republic"
        ], attrgetter("name"))

        created = Country.objects.bulk_create([])
        self.assertEqual(created, [])
        self.assertEqual(Country.objects.count(), 4)

    def test_efficiency(self):
        with self.assertNumQueries(1):
            Country.objects.bulk_create(self.data)

    def test_inheritance(self):
        Restaurant.objects.bulk_create([
            Restaurant(name="Nicholas's")
        ])
        self.assertQuerysetEqual(Restaurant.objects.all(), [
            "Nicholas's",
        ], attrgetter("name"))
        with self.assertRaises(ValueError):
            Pizzeria.objects.bulk_create([
                Pizzeria(name="The Art of Pizza")
            ])
        self.assertQuerysetEqual(Pizzeria.objects.all(), [])
        self.assertQuerysetEqual(Restaurant.objects.all(), [
            "Nicholas's",
        ], attrgetter("name"))

    def test_non_auto_increment_pk(self):
        with self.assertNumQueries(1):
            State.objects.bulk_create([
                State(two_letter_code=s)
                for s in ["IL", "NY", "CA", "ME"]
            ])
        self.assertQuerysetEqual(State.objects.order_by("two_letter_code"), [
            "CA", "IL", "ME", "NY",
        ], attrgetter("two_letter_code"))

    def test_large_batch(self):
        with override_settings(DEBUG=True):
            connection.queries = []
            TwoFields.objects.bulk_create([
                   TwoFields(f1=i, f2=i+1) for i in range(0, 1001)
                ])
            self.assertTrue(len(connection.queries) < 10)
        self.assertEqual(TwoFields.objects.count(), 1001)
        self.assertEqual(
            TwoFields.objects.filter(f1__gte=450, f1__lte=550).count(),
            101)
        self.assertEqual(TwoFields.objects.filter(f2__gte=901).count(), 101)

    def test_large_batch_mixed(self):
        """
        Test inserting a large batch with objects having primary key set
        mixed together with objects without PK set.
        """
        with override_settings(DEBUG=True):
            connection.queries = []
            TwoFields.objects.bulk_create([
                TwoFields(id=i if i % 2 == 0 else None, f1=i, f2=i+1)
                for i in range(100000, 101000)])
            self.assertTrue(len(connection.queries) < 10)
        self.assertEqual(TwoFields.objects.count(), 1000)
        # We can't assume much about the ID's created, except that the above
        # created IDs must exist.
        id_range = range(100000, 101000, 2)
        self.assertEqual(TwoFields.objects.filter(id__in=id_range).count(), 500)
        self.assertEqual(TwoFields.objects.exclude(id__in=id_range).count(), 500)

    def test_explicit_batch_size(self):
        objs = [TwoFields(f1=i, f2=i) for i in range(0, 100)]
        with self.assertNumQueries(2):
            TwoFields.objects.bulk_create(objs, 50)
        TwoFields.objects.all().delete()
        with self.assertNumQueries(1):
            TwoFields.objects.bulk_create(objs, len(objs))
