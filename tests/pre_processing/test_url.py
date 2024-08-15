from unittest import TestCase

from metal.pre_processing.url import Url


class UrlTests(TestCase):
    def test_from_text__https(self):
        urls = Url.from_text('Visit https://www.metal.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://www.metal.ai/', span=(6, 28))
        ])

    def test_from_text__http(self):
        urls = Url.from_text('Visit http://www.metal.ai/.')
        self.assertListEqual(urls, [
            Url(text='http://www.metal.ai/', span=(6, 27))
        ])

    def test_from_text__no_protocol(self):
        urls = Url.from_text('Visit www.metal.ai.')
        self.assertListEqual(urls, [
            Url(text='www.metal.ai', span=(6, 19))
        ])

    def test_from_text__no_trailing_slash(self):
        urls = Url.from_text('Visit https://www.metal.ai.')
        self.assertListEqual(urls, [
            Url(text='https://www.metal.ai', span=(6, 27))
        ])

    def test_from_text__path(self):
        urls = Url.from_text('Visit https://www.metal.ai/team/.')
        self.assertListEqual(urls, [
            Url(text='https://www.metal.ai/team/', span=(6, 33))
        ])

    def test_from_text__args(self):
        urls = Url.from_text('Visit https://www.metal.ai/?var1=1&var2=2.')
        self.assertListEqual(urls, [
            Url(text='https://www.metal.ai/?var1=1&var2=2', span=(6, 42))
        ])

    def test_from_text__custom_sub_domain(self):
        urls = Url.from_text('Visit https://custom.metal.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://custom.metal.ai/', span=(6, 31))
        ])

    def test_from_text__custom_domain_extension(self):
        urls = Url.from_text('Visit https://www.metal.abc/.')
        self.assertListEqual(urls, [
            Url(text='https://www.metal.abc/', span=(6, 29))
        ])

    def test_from_text__multiple(self):
        urls = Url.from_text('Visit https://one.metal.ai/ and https://two.metal.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://one.metal.ai/', span=(6, 28)),
            Url(text='https://two.metal.ai/', span=(33, 55))
        ])
