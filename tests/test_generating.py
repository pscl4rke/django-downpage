

import unittest

from downpage import generating


class TestListOfPages(unittest.TestCase):

    def test_when_misconfigured(self):
        class Settings:
            pass  # not set
        with self.assertRaises(generating.ImproperlyConfigured):
            generating.get_pages_to_generate(Settings())

    def test_getting_pages(self):
        class Settings:
            DOWNPAGE_PAGES = [("foo", "bar")]
        pages = generating.get_pages_to_generate(Settings())
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0][0], "foo")
        self.assertEqual(pages[0][1], "bar")

    def test_extra_context(self):
        class Settings:
            DOWNPAGE_PAGES = [
                ("foo", "FOO"),
                ("bar", "BAR", {"hello": "world"}),
            ]
        pages = generating.get_pages_to_generate(Settings())
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0][2], {})
        self.assertEqual(pages[1][2]["hello"], "world")
