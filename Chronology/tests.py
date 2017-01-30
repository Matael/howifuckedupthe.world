from django.test import TestCase

import wikipedia
import datetime

from .models import Function, Person, Event

FUNCTIONS = [
    "President of the USA",
    "Duke of Arrakis",
    "Sith Emperor"
]

PERSONS = [
    "Henri Poincaré",
    "Julius Caesar",
    "Someone That Doesn't Exist"
]

class TestModel_Function(TestCase):

    def test_add(self):
        """Test if adding works and if string serialization is not fucked up"""

        functions = [
            "President of the USA",
            "Duke of Arrakis",
            "Sith Emperor"
        ]

        for f in FUNCTIONS:
            saved_f = Function.objects.create(name=f)

            test_f = Function.objects.get(pk=saved_f.id)
            self.assertEqual(str(saved_f), f)


class TestModel_Person(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.functions = [Function.objects.create(name=_) for _ in FUNCTIONS]


    def test_add(self):
        """Test if adding works and if string serialization is not fucked up"""

        for i_p,pname in enumerate(PERSONS):

            p = Person.objects.create(name=pname)
            p.functions.add(self.functions[i_p%len(FUNCTIONS)])
            p.save()
            the_id = p.id

            del p
            p = Person.objects.get(pk=the_id)

            wppages = wikipedia.search(pname)
            wikipedia_summary = wikipedia.summary(wppages[0]) if wppages else ''

            self.assertEqual(str(p), pname)
            self.assertEqual(p.wiki_summary, wikipedia_summary)
            for f in p.functions.all():
                self.assertIn(f.name, FUNCTIONS)


class TestModel_Event(TestCase):

    def test_add(self):
        """Test if adding works and if string serialization is not fucked up"""

        f = Function.objects.create(name='King of Doom')

        p_name = PERSONS[2]
        p = Person.objects.create(name=p_name)
        p.functions.add(f)
        p.save()

        today = datetime.date.today()
        e = Event()
        e.date = today
        e.name ='Became an asshole'
        e.who = p
        e.function_at_the_time = p.functions.all()[0]
        e.description = 'This is a description.'
        e.save()

        the_id = e.id
        del e
        e = Event.objects.get(pk=the_id)

        self.assertEqual(e.name, 'Became an asshole')
        self.assertEqual(str(e.who), p_name)
        self.assertEqual(e.function_at_the_time.name, f.name)
        self.assertEqual(e.description, 'This is a description.')
        self.assertEqual(e.date, today)
        self.assertEqual(str(e), 'Became an asshole by %s on the %s'%(p_name, today))


    def test_add_function(self):
        """ When adding an event, if the Function is not part of the Person's record, add
        it"""

        f = Function.objects.create(name='King of Doom')
        f2 = Function.objects.create(name=FUNCTIONS[0])

        p_name = PERSONS[2]
        p = Person.objects.create(name=p_name)
        p.functions.add(f)
        p.save()


        today = datetime.date.today()
        e = Event()
        e.date = today
        e.name ='Became an asshole'
        e.who = p
        e.function_at_the_time = f2
        e.description = 'This is a description.'
        e.save()

        the_id = e.id
        del e
        e = Event.objects.get(pk=the_id)

        self.assertIn(f2, p.functions.all())

