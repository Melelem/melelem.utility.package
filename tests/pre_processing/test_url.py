from unittest import TestCase

from soffos.pre_processing import TextSpan
from soffos.pre_processing.url import get_urls


class Tests(TestCase):
    def test_https(self):
        urls = get_urls('Visit https://www.soffos.ai/.')
        self.assertListEqual(urls, [
            TextSpan(text='https://www.soffos.ai/', span=(6, 28))
        ])

    def test_http(self):
        urls = get_urls('Visit http://www.soffos.ai/.')
        self.assertListEqual(urls, [
            TextSpan(text='http://www.soffos.ai/', span=(6, 27))
        ])

    def test_no_protocol(self):
        urls = get_urls('Visit www.soffos.ai.')
        self.assertListEqual(urls, [
            TextSpan(text='www.soffos.ai', span=(6, 19))
        ])

    def test_no_trailing_slash(self):
        urls = get_urls('Visit https://www.soffos.ai.')
        self.assertListEqual(urls, [
            TextSpan(text='https://www.soffos.ai', span=(6, 27))
        ])

    def test_path(self):
        urls = get_urls('Visit https://www.soffos.ai/team/.')
        self.assertListEqual(urls, [
            TextSpan(text='https://www.soffos.ai/team/', span=(6, 33))
        ])

    def test_args(self):
        urls = get_urls('Visit https://www.soffos.ai/?var1=1&var2=2.')
        self.assertListEqual(urls, [
            TextSpan(text='https://www.soffos.ai/?var1=1&var2=2', span=(6, 42))
        ])

    def test_custom_sub_domain(self):
        urls = get_urls('Visit https://custom.soffos.ai/.')
        self.assertListEqual(urls, [
            TextSpan(text='https://custom.soffos.ai/', span=(6, 31))
        ])

    def test_custom_domain_extension(self):
        urls = get_urls('Visit https://www.soffos.abc/.')
        self.assertListEqual(urls, [
            TextSpan(text='https://www.soffos.abc/', span=(6, 29))
        ])

    def test_multiple(self):
        urls = get_urls('Visit https://one.soffos.ai/ and https://two.soffos.ai/.')
        self.assertListEqual(urls, [
            TextSpan(text='https://one.soffos.ai/', span=(6, 28)),
            TextSpan(text='https://two.soffos.ai/', span=(33, 55))
        ])
