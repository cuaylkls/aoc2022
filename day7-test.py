import unittest
import day7


class VFSErrorTestCase(unittest.TestCase):
    def test_raise(self):
        def raise_error():
            raise day7.VFSError("testing")

        # test raise
        self.assertRaises(
            day7.VFSError,
            raise_error
        )

        # test message
        try:
            raise_error()
        except day7.VFSError as e:
            self.assertEqual(e.message, "testing")


class VFsObjectTestCase(unittest.TestCase):
    def test_invalid_name_chars(self):
        """ Test that names line break characters are rejected"""
        with self.assertRaises(day7.VFSError) as cm:
            day7.VFsObject("test\n", None)

        e: day7.VFSError = cm.exception
        self.assertEqual(e.message, "Filesystem object names must not contain newline characters.")

        with self.assertRaises(day7.VFSError) as cm:
            day7.VFsObject("test\r\n", None)

        e: day7.VFSError = cm.exception
        self.assertEqual(e.message, "Filesystem object names must not contain newline characters.")


class CommandLineTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(day7.CommandLine(), day7.CommandLine)

    def test_process_command_line(self):
        def command_order():
            cmd = day7.CommandLine()
            cmd.process_command_line("command order test")

        # process a command output before inside a command
        with self.assertRaises(day7.VFSError) as cm:
            command_order()

            e: day7.VFSError = cm.exception
            self.assertEqual(e.message, "Cannot process output outside a command.")

    def test_run_command(self):
        cmd = day7.CommandLine()

        # running an invalid command raises an exception
        self.assertRaises(
            day7.VFSError,
            lambda: cmd.run_command("unknown 1123")
        )

    def test_run_command_cd(self):
        cmd = day7.CommandLine()

        cmd.run_command("cd /")
        self.assertEqual(cmd.cur_dir.path, "/")

        cmd.run_command("cd test")
        self.assertEqual(cmd.cur_dir.path, "/test")

        cmd.run_command("cd ..")
        self.assertEqual(cmd.cur_dir.path, "/", msg="Test cd to parent directory")

        self.assertRaises(
            NotImplementedError,
            lambda: cmd.run_command("cd /test/dir/subdir")
        )

    def test_run_command_ls(self):
        cmd = day7.CommandLine()
        cmd.run_command("cd /")

        # check that process is recognised as being inside a command
        cmd.run_command("ls")
        self.assertTrue(cmd.in_cmd)

        # check trying to run another command raises an error
        self.assertRaises(
            day7.VFSError,
            lambda: cmd.run_command("ls")
        )

        # check not implemented is returned
        del cmd
        cmd = day7.CommandLine()
        cmd.run_command("cd /")
        self.assertRaises(
            NotImplementedError,
            lambda: cmd.run_command("ls /some/other/directory")
        )

        cmd.process_command_line("$ ls")
        cmd.process_command_line("272080 adam.hdr")
        cmd.process_command_line("dir fred")
        cmd.process_command_line("6067 harry")

        files = cmd.file_system.children

        # check types of child items
        self.assertIsInstance(files[0], day7.VFile)
        self.assertIsInstance(files[1], day7.VDirectory)
        self.assertIsInstance(files[2], day7.VFile)

        # check paths are correct
        self.assertEqual(files[0].path, "/adam.hdr")
        self.assertEqual(files[1].path, "/fred")
        self.assertEqual(files[2].path, "/harry")

        # check file sizes
        self.assertEqual(files[0].size, 272080)
        self.assertEqual(files[2].size, 6067)


    #  test_process_line(self):
    #    cmd = day7.CommandLine()
    #    cmd.process_command_line("$ cd /")


class VFileTestCase(unittest.TestCase):
    def test_init(self):
        class DummyObj(object):
            pass

        v_dir = day7.VDirectory("/")

        # create with no parent
        self.assertIsInstance(day7.VFile("name", 0), day7.VFile)
        self.assertIsInstance(day7.VFile("name", 0,  v_dir), day7.VFile)

        # wrong parent type test
        self.assertRaises(
            TypeError,
            lambda: day7.VFile("name", 0, DummyObj())
        )

        # size is not an integer
        self.assertRaises(
            TypeError,
            lambda: day7.VFile("name", "s")
        )

        # size is less than zero
        self.assertRaises(
            ValueError,
            lambda: day7.VFile("name", -1)
        )

    def test_path(self):
        v_dir = day7.VDirectory("/")
        v_file = day7.VFile("my_file", 0, v_dir)

        self.assertEqual(v_file.path, "/my_file")

        v_file2 = day7.VFile("my_file2", 0)
        self.assertEqual(v_file2.path, "my_file2")

    def test_name(self):
        v_file = day7.VFile("my_file", 0)

        # test file name
        self.assertEqual(v_file.name, "my_file")

    def test_parent_dir(self):
        # no parent
        self.assertIsNone(day7.VFile("no_parent", 0).parent)

        v_dir = day7.VDirectory("/")
        v_file = day7.VFile("my_file", 0, v_dir)
        self.assertEqual(v_file.parent, v_dir)

        # assigning a parent dir
        v_file2 = day7.VFile("other", 0)
        v_file2.parent = v_dir

        self.assertTrue(v_file2.parent, v_dir)

        # test removal of parent
        v_file2.parent = None
        self.assertIsNone(v_file2.parent)

    def test_size(self):
        size = 1943
        v_file = day7.VFile("my_file", size)
        self.assertEqual(v_file.size, size)


class VDirectoryTestCase(unittest.TestCase):
    @staticmethod
    def common_setup():
        # tests init as root v_dir
        v_dir = day7.VDirectory("/")

        # initilise with a parent directory
        v_dir2 = day7.VDirectory("subdir", v_dir)
        v_dir3 = day7.VDirectory("subdir2", v_dir)
        v_dir4 = day7.VDirectory("no_parent")

        return v_dir, v_dir2, v_dir3, v_dir4

    def test_init(self):
        class DummyObj(object):
            pass

        # tests init as root v_dir
        v_dir = day7.VDirectory("/")
        self.assertEqual(v_dir.name, "/")

        # initilise with a parent directory
        v_dir2 = day7.VDirectory("subdir", v_dir)
        self.assertIsInstance(v_dir2.parent, day7.VDirectory)

        # initilise with the wrong parent_dir type
        self.assertRaises(
            TypeError,
            lambda: day7.VDirectory("subdir", DummyObj)
        )

    def test_name(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        # test root dir name
        self.assertEqual(v_dir.name, "/")

        # initilise with a parent directory
        self.assertEqual(v_dir2.name, "subdir")

    def test_is_root(self):
        v_dir = day7.VDirectory("/")
        self.assertTrue(v_dir.is_root)

    def test_path(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        self.assertEqual(v_dir.path, "/")  # root only
        self.assertEqual(v_dir4.path, "no_parent")  # no parent dir
        self.assertEqual(v_dir2.path, "/subdir")  # sub directory

        v_dir5 = day7.VDirectory("subdir2", v_dir4)  # parent with no root
        self.assertEqual(v_dir5.path, "no_parent/subdir2")

    def test_parent_dir(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        # root dir has no parent
        self.assertIsNone(v_dir.parent)

        # correct parent dir for child
        self.assertEqual(v_dir2.parent, v_dir)

        # assigning a parent dir
        v_dir4.parent = v_dir
        self.assertTrue(v_dir4.parent, v_dir)

        # test removal of parent
        v_dir3.parent = None
        self.assertIsNone(v_dir.parent)

    def test_children(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        # no children
        self.assertEqual(v_dir2.children, [])

        # children
        self.assertEqual(v_dir.children, [v_dir2, v_dir3])

        # assigning a parent dir
        v_dir4.parent = v_dir
        self.assertEqual(v_dir4.parent, v_dir)
        self.assertEqual(v_dir.children, [v_dir2, v_dir3, v_dir4])

        # removing a parent dir
        v_dir4.parent = None
        self.assertEqual(v_dir.children, [v_dir2, v_dir3])

    def test_add_child(self):
        class DummyObj(object):
            pass

        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        # add directory child
        v_dir.add_child(v_dir4)
        self.assertEqual(v_dir.children, [v_dir2, v_dir3, v_dir4])

        v_file = day7.VFile("name", 0, v_dir)
        self.assertEqual(
            v_dir.children, [v_dir2, v_dir3, v_dir4, v_file]
        )

        self.assertRaises(
            TypeError,
            lambda: v_dir.add_child(DummyObj())
        )

    def test_add_child_no_duplicates(self):
        """ Add child check no duplicates """

        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        def add_duplicate_child():
            day7.VDirectory("subdir", v_dir)

        with self.assertRaises(day7.VFSError) as cm:
            add_duplicate_child()

        e: day7.VFSError = cm.exception
        self.assertTrue(e.message.startswith("Cannot add child with duplicate name"))

    def test_remove_child(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        # remove existing child
        v_dir.remove_child(v_dir2)
        self.assertEqual(
            v_dir.children,
            [v_dir3, ]
        )
        # remove child that does not exists
        self.assertRaises(
            ValueError,
            lambda: v_dir.remove_child(v_dir4)
        )

    def test_size(self):
        v_dir, v_dir2, v_dir3, v_dir4 = self.common_setup()

        day7.VFile("file1", 10, v_dir)
        day7.VFile("file2", 20, v_dir)
        day7.VFile("file3", 30, v_dir)

        # directory with only file
        self.assertEqual(60, v_dir.size)

        # sub directory
        day7.VFile("file1", 10, v_dir2)
        day7.VFile("file2", 20, v_dir2)
        self.assertEqual(30, v_dir2.size)

        # size with sub-dirs and files
        self.assertEqual(90, v_dir.size)


if __name__ == '__main__':
    unittest.main()
