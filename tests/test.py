import sys
sys.path.append('../')

from extract2blade import ExtractToBlade 

import unittest
import os
# https://stackoverflow.com/a/652299/4330182
class Test(object):
    def __new__(cls, **attrs):
        result = object.__new__(cls)
        result.__dict__ = attrs
        return result

class TestPathsMethods(unittest.TestCase):
    def test_1(self):
        tests = [
            Test(
                input="welcome",
                path=os.path.normpath('/path/to/resources/views/'),
                output_directory=os.path.normpath('/path/to/resources/views/'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/welcome.blade.php'),
                blade_filepath="welcome",
                blade_dirpath="",
            ),
            Test(
                input="wel/foo/bar",
                path=os.path.normpath('/path/to/resources/views/'),
                output_directory=os.path.normpath('/path/to/resources/views/wel/foo'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/wel/foo/bar.blade.php'),
                blade_filepath="wel.foo.bar",
                blade_dirpath="wel/foo/",
            ),
            Test(
                input="wel.foo.bar",
                path=os.path.normpath('/path/to/resources/views/'),
                output_directory=os.path.normpath('/path/to/resources/views/wel/foo'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/wel/foo/bar.blade.php'),
                blade_filepath="wel.foo.bar",
                blade_dirpath="wel.foo.",
            ),
            Test(
                input="wel/FOo.bar",
                path=os.path.normpath('/path/to/aresources/viewS/'),
                output_directory=os.path.normpath('/path/to/aresources/viewS/wel/FOo'),
                absolute_filepath=os.path.normpath('/path/to/aresources/viewS/wel/FOo/bar.blade.php'),
                blade_filepath="wel.foo.bar",
                blade_dirpath="wel/FOo.",
            ),
            Test(
                input="/moh/FOo.bar",
                path=os.path.normpath('/path/to/aresources/viewS/'),
                output_directory=os.path.normpath('/path/to/aresources/viewS/moh/FOo'),
                absolute_filepath=os.path.normpath('/path/to/aresources/viewS/moh/FOo/bar.blade.php'),
                blade_filepath="moh.foo.bar",
                blade_dirpath="/moh/FOo.",
            ),
            Test(
                input="\\hello/foo.bar",
                path=os.path.normpath('/path/to/aresources/viewS/'),
                output_directory=os.path.normpath('/path/to/aresources/viewS/hello/foo'),
                absolute_filepath=os.path.normpath('/path/to/aresources/viewS/hello/foo/bar.blade.php'),
                blade_filepath="hello.foo.bar",
                blade_dirpath="\\hello/foo.",
            ),
            Test(
                input="../hello/foo.bar",
                path=os.path.normpath('/path/to/resources/views/relative/'),
                output_directory=os.path.normpath('/path/to/resources/views/hello/foo'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/hello/foo/bar.blade.php'),
                blade_filepath="hello.foo.bar",
                blade_dirpath="../hello/foo.",
            ),
            Test(
                input="hello/foo.bar.hi",
                path=os.path.normpath('/path/to/resources/views/'),
                output_directory=os.path.normpath('/path/to/resources/views/hello/foo/bar'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/hello/foo/bar/hi.blade.php'),
                blade_filepath="hello.foo.bar.hi",
                blade_dirpath="hello/foo.bar.",
            ),
            Test(
                input="../../welcome.modal",
                path=os.path.normpath('/path/to/resources/views/shared/layouts'),
                output_directory=os.path.normpath('/path/to/resources/views/welcome'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/welcome/modal.blade.php'),
                blade_filepath="welcome.modal",
                blade_dirpath="../../welcome.",
            ),
            Test(
                input="../../welcome.partials.modal",
                path=os.path.normpath('/path/to/resources/views/shared/layouts'),
                output_directory=os.path.normpath('/path/to/resources/views/welcome/partials'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/welcome/partials/modal.blade.php'),
                blade_filepath="welcome.partials.modal",
                blade_dirpath="../../welcome.partials.",
            ),
            Test(
                input="header",
                path=os.path.normpath('/path/to/resources/views/layouts/'),
                output_directory=os.path.normpath('/path/to/resources/views/layouts'),
                absolute_filepath=os.path.normpath('/path/to/resources/views/layouts/header.blade.php'),
                blade_filepath="layouts.header",
                blade_dirpath="",
            ),
            Test(
                input="../header",
                path=os.path.normpath('/path/to/resources/_views/layouts/'),
                output_directory=os.path.normpath('/path/to/resources/_views/'),
                absolute_filepath=os.path.normpath('/path/to/resources/_views/header.blade.php'),
                blade_filepath="", # Can't resolve blade path!
                blade_dirpath="../",
            ),
        ]

        for test in tests:
            output_directory = ExtractToBlade.get_output_directory(test.path, test.input)
            absolute_filepath = ExtractToBlade.get_absolute_filepath(test.path, test.input)
            blade_filepath = ExtractToBlade.get_blade_filepath(test.path, test.input)
            blade_dirpath = ExtractToBlade.get_blade_dirpath(test.path, test.input)
            if not test.output_directory == False:
                self.assertEqual(output_directory, test.output_directory)
            if not test.absolute_filepath == False:
                self.assertEqual(absolute_filepath, test.absolute_filepath)
            if not test.blade_filepath == False:
                self.assertEqual(blade_filepath, test.blade_filepath)
            if not test.blade_dirpath == False:
                self.assertEqual(blade_dirpath, test.blade_dirpath)
