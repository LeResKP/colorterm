import unittest
import sys
from colorterm.colorterm import parse_attr, applycolor, formatter
from colorterm import colorterm


class TestColorTerm(unittest.TestCase):

    def setUp(self):
        self.old_isatty = sys.stdout.isatty
        sys.stdout.isatty = lambda: True

    def tearDown(self):
        sys.stdout.isatty = self.old_isatty

    def test_formatter(self):
        res = formatter('{red}{underline}Hello{/underline} world')
        expected = '\x1b[31m\x1b[4mHello\x1b[24m world\x1b[0m'
        self.assertEqual(res, expected)

        res = formatter('{red}{underline}Hello{reset} world')
        expected = '\x1b[31m\x1b[4mHello\x1b[0m world\x1b[0m'
        self.assertEqual(res, expected)

        res = formatter('{on_green}{red}Hello{/red}{/on_green} world')
        expected = '\x1b[42m\x1b[31mHello\x1b[39m\x1b[49m world\x1b[0m'
        self.assertEqual(res, expected)

    def test_formatter_no_tty(self):
        sys.stdout.isatty = self.old_isatty
        res = formatter('{red}{underline}Hello{/underline} world')
        expected = 'Hello world'
        self.assertEqual(res, expected)

    def test_parse_attr(self):
        res = parse_attr('underline')
        self.assertEqual(res, {
            'formatting': 4,
            'bgcolor': None,
            'fgcolor': None
        })

        res = parse_attr('red')
        self.assertEqual(res, {
            'formatting': None,
            'bgcolor': None,
            'fgcolor': 31
        })

        res = parse_attr('on_green')
        self.assertEqual(res, {
            'formatting': None,
            'bgcolor': 42,
            'fgcolor': None
        })

        res = parse_attr('underline_red')
        self.assertEqual(res, {
            'formatting': 4,
            'bgcolor': None,
            'fgcolor': 31
        })

        res = parse_attr('underline_on_green')
        self.assertEqual(res, {
            'formatting': 4,
            'bgcolor': 42,
            'fgcolor': None
        })

        res = parse_attr('underline_red_on_green')
        self.assertEqual(res, {
            'formatting': 4,
            'bgcolor': 42,
            'fgcolor': 31
        })

        res = parse_attr('red_on_green')
        self.assertEqual(res, {
            'formatting': None,
            'bgcolor': 42,
            'fgcolor': 31
        })

        try:
            parse_attr('unexisting_on_green')
            assert(False)
        except Exception as e:
            self.assertEqual(str(e), 'Bad attribute: unexisting')

        try:
            parse_attr('red_on_unexisting')
            assert(False)
        except Exception as e:
            self.assertEqual(str(e), 'Bad background color: unexisting')

    def test_applycolor(self):
        res = applycolor('Hello world', formatting=4, bgcolor=42, fgcolor=31)
        expected = '\x1b[4;42;31mHello world\x1b[0m'
        self.assertEqual(res, expected)

        res = applycolor('Hello world')
        self.assertEqual(res, 'Hello world')

        res = applycolor('Hello world', fgcolor=31)
        expected = '\x1b[31mHello world\x1b[0m'
        self.assertEqual(res, expected)

    def test_applycolor_no_tty(self):
        sys.stdout.isatty = self.old_isatty
        res = applycolor('Hello world', formatting=4, bgcolor=42, fgcolor=31)
        expected = 'Hello world'
        self.assertEqual(res, expected)

    def test_colorterm(self):
        res = colorterm.underline_red_on_green('Hello world')
        expected = '\x1b[4;42;31mHello world\x1b[0m'
        self.assertEqual(res, expected)

        res = colorterm.red_on_green('Hello world')
        expected = '\x1b[42;31mHello world\x1b[0m'
        self.assertEqual(res, expected)

        res = colorterm.on_green('Hello world')
        expected = '\x1b[42mHello world\x1b[0m'
        self.assertEqual(res, expected)

        res = colorterm.red('Hello world')
        expected = '\x1b[31mHello world\x1b[0m'
        self.assertEqual(res, expected)

        res = colorterm.underline('Hello world')
        expected = '\x1b[4mHello world\x1b[0m'
        self.assertEqual(res, expected)
