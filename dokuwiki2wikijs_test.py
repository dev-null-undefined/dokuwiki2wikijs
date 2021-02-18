import unittest

from dokuwiki2wikijs import first_heading_or_filename, convert_filename_to_unicode, convert_wrap, unwrap_sentences


class Dokuwiki2WikijsTest(unittest.TestCase):

    def test_get_title(self):
        lines = ["# Title"]
        self.assertEqual(first_heading_or_filename(lines, ""), "Title")

        lines = ["# Title with spaces"]
        self.assertEqual(first_heading_or_filename(
            lines, ""), "Title with spaces")

        lines = ["some other text on the first line"]
        self.assertEqual(first_heading_or_filename(
            lines, "Some other title"), "Some other title")

    def test_convert_to_unicode(self):
        self.assertEqual(convert_filename_to_unicode(
            "a%C3%96bcdef"), "aÖbcdef")
        self.assertEqual(convert_filename_to_unicode(
            "abc%C3%B6def"), "abcödef")
        self.assertEqual(convert_filename_to_unicode(
            "a%C3%B6bcdef"), "aöbcdef")

    def test_convert_wrap_can_pass_through(self):
        lines = ["no WRAP here"]
        self.assertEqual(convert_wrap(lines), ["no WRAP here"])

    def test_convert_simple_wrap_on_separate_first_lines(self):
        lines = ["<WRAP>", "</WRAP>"]
        self.assertEqual(convert_wrap(lines), ["> ", "{.is-info}"])

    def test_convert_simple_wrap_on_separate_lines(self):
        lines = ["", "<WRAP>", "</WRAP>"]
        self.assertEqual(convert_wrap(lines), ["", "> ", "{.is-info}"])

    def test_convert_simple_alert_wrap_on_separate_lines(self):
        lines = ["", "<WRAP alert>", "</WRAP>"]
        self.assertEqual(convert_wrap(lines), ["", "> ", "{.is-danger}"])

    def test_convert_wrap_on_one_line(self):
        lines = ["<WRAP>one line wrap</WRAP>"]
        self.assertEqual(convert_wrap(lines), ["> one line wrap{.is-info}"])

    def test_convert_escaped_wrap(self):
        lines = ["\<WRAP\>", "one line", "\</WRAP\>"]
        self.assertEqual(convert_wrap(lines), ["> ", "one line", "{.is-info}"])

    def test_unwrap_single_line(self):
        lines = ["A single line."]
        self.assertEqual(unwrap_sentences(lines), ["A single line."])

    def test_unwrap_empty_line(self):
        lines = [""]
        self.assertEqual(unwrap_sentences(lines), [""])

    def test_unwrap_two_sentences_on_same_line(self):
        lines = ["A sentence. And another."]
        self.assertEqual(unwrap_sentences(lines), [
                         "A sentence.", "And another."])

    def test_unwrap_incomplete_sentences_to_same_line(self):
        lines = ["A sentence", "which continues on the next line."]
        self.assertEqual(unwrap_sentences(lines), [
            "A sentence which continues on the next line."])

    def test_unwrap_multiple_incomplete_sentences_to_same_line(self):
        lines = ["A sentence",
                 "which continues. With another on the next", "line."]
        self.assertEqual(unwrap_sentences(lines), [
            "A sentence which continues.", "With another on the next line."])

    def test_does_not_unwrap_if_next_line_starts_with_non_alfa(self):
        lines = ["A sentence", " which continues on the next line."]
        self.assertEqual(unwrap_sentences(lines), [
            "A sentence", " which continues on the next line."])
