from unittest import TestCase

from soffos.pre_processing.url import Url


class UrlTests(TestCase):
    def test_from_text__https(self):
        urls = Url.from_text('Visit https://www.soffos.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://www.soffos.ai/', span=(6, 28))
        ])

    def test_from_text__http(self):
        urls = Url.from_text('Visit http://www.soffos.ai/.')
        self.assertListEqual(urls, [
            Url(text='http://www.soffos.ai/', span=(6, 27))
        ])

    def test_from_text__no_protocol(self):
        urls = Url.from_text('Visit www.soffos.ai.')
        self.assertListEqual(urls, [
            Url(text='www.soffos.ai', span=(6, 19))
        ])

    def test_from_text__no_trailing_slash(self):
        urls = Url.from_text('Visit https://www.soffos.ai.')
        self.assertListEqual(urls, [
            Url(text='https://www.soffos.ai', span=(6, 27))
        ])

    def test_from_text__path(self):
        urls = Url.from_text('Visit https://www.soffos.ai/team/.')
        self.assertListEqual(urls, [
            Url(text='https://www.soffos.ai/team/', span=(6, 33))
        ])

    def test_from_text__args(self):
        urls = Url.from_text('Visit https://www.soffos.ai/?var1=1&var2=2.')
        self.assertListEqual(urls, [
            Url(text='https://www.soffos.ai/?var1=1&var2=2', span=(6, 42))
        ])

    def test_from_text__custom_sub_domain(self):
        urls = Url.from_text('Visit https://custom.soffos.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://custom.soffos.ai/', span=(6, 31))
        ])

    def test_from_text__custom_domain_extension(self):
        urls = Url.from_text('Visit https://www.soffos.abc/.')
        self.assertListEqual(urls, [
            Url(text='https://www.soffos.abc/', span=(6, 29))
        ])

    def test_from_text__multiple(self):
        urls = Url.from_text('Visit https://one.soffos.ai/ and https://two.soffos.ai/.')
        self.assertListEqual(urls, [
            Url(text='https://one.soffos.ai/', span=(6, 28)),
            Url(text='https://two.soffos.ai/', span=(33, 55))
        ])
