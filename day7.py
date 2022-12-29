import re


class VFSError(Exception):
    @property
    def message(self) -> str:
        return self._message

    def __init__(self, message):
        super(VFSError, self).__init__(message)
        self._message = message


class VFsObject:
    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._set_parent(new_parent)

    @property
    def path(self):
        if self._parent is None:
            return self._name
        else:
            if self._parent.is_root:
                return f"/{self._name}"
            else:
                return f"{self._parent.path}/{self._name}"

    def __init__(self, obj_name, parent_dir):
        if not isinstance(parent_dir, VDirectory) and parent_dir is not None:
            raise TypeError(f"Invalid type passed to parent_dir argument. "
                            f"Excepting {VDirectory} got {type(parent_dir)}")

        if re.search("[\r\n]", obj_name) is not None:
            raise VFSError("Filesystem object names must not contain newline characters.")

        self._name = obj_name
        self._parent = None
        self._set_parent(parent_dir)

    def _set_parent(self, new_parent):
        if (not isinstance(new_parent, VDirectory)) and \
                new_parent is not None:
            raise TypeError(f"Invalid type passed to new_parent argument. "
                            f"Excepting {type(self)} got {type(new_parent)}")

        if self._parent is not None:
            self._parent.remove_child(self)

        if new_parent is None:
            self._parent = None
        else:
            self._parent = new_parent
            new_parent.add_child(self)

    def __repr__(self):
        return f"{type(self).__name__}(\"{self.name}\", {self._parent})"

    def __str__(self):
        return self.path


class VFile(VFsObject):

    @property
    def size(self):
        return self._size

    def __init__(self, file_name, size, parent_dir=None):
        if not isinstance(size, int):
            raise TypeError(f"Wrong data type for size, expecting int, got {type(size)}")

        if size < 0:
            raise ValueError("Size must not be a negative number.")

        self._size = size

        super(VFile, self).__init__(file_name, parent_dir)


class VDirectory(VFsObject):

    @property
    def is_root(self):
        return self._is_root

    @property
    def children(self):
        return self._children

    @property
    def size(self):
        if self._size is None:
            size = 0
            for item in self.children:
                size += item.size

            self._size = size

        return self._size

    def add_child(self, child_obj: VFsObject):
        if not isinstance(child_obj, VFsObject):
            raise TypeError(f"Invalid type passed to child_dir argument. "
                            f"Excepting {type(self)} got {type(child_obj)}")

        for child in self._children:
            if child.name == child_obj.name:
                raise VFSError(f"Cannot add child with duplicate name: {child_obj.name}")

        self._children.append(child_obj)
        self.recalculate_size()
        return child_obj

    def remove_child(self, child_dir):
        self._children.remove(child_dir)
        self.recalculate_size()

    def has_child(self, child_name: str) -> bool:
        for child in self._children:
            if child.name == child_name:
                return True

        return False

    def get_child(self, child_name: str) -> VFsObject:
        for child in self._children:
            if child.name == child_name:
                return child

    def recalculate_size(self, force=False):
        if self._size is None and not force:
            return  # only reset size if not already reset

        parent_dir: VDirectory = self.parent
        self._size = None

        while parent_dir is not None:
            parent_dir.recalculate_size()
            parent_dir = parent_dir.parent

    def __init__(self, dir_name, parent_dir=None):
        self._children = []
        self._size = None

        if dir_name == "/":
            self._is_root = True
        else:
            self._is_root = False

        super(VDirectory, self).__init__(dir_name, parent_dir)


class CommandLine:
    @property
    def file_system(self):
        return self._top_dir

    @property
    def cur_dir(self):
        return self._cur_dir

    @property
    def in_cmd(self):
        return self._in_cmd

    def __init__(self):
        self._cur_dir: VDirectory = None
        self._top_dir: VDirectory = None
        self._in_cmd = False
        self._output_processor = None

    def _cmd_ls_output_processor(self, output_line):
        parts = output_line.split(" ")
        item_name = parts[1].strip()

        if self._cur_dir.has_child(item_name):
            return

        if parts[0] == "dir":
            VDirectory(item_name, self._cur_dir)
        else:
            VFile(item_name, int(parts[0]), self._cur_dir)

    def _cmd_ls(self, line):
        if line is not None:
            raise NotImplementedError("ls for other directories are not currently supported")

        self._in_cmd = True
        return self._cmd_ls_output_processor

    def _cmd_cd(self, line):
        arg_dir = line.strip()

        if arg_dir.count("/") > 1 and arg_dir != "/":
            raise NotImplementedError("Multiple directory cd not yet supported")

        # no forward slashes in path
        if self._cur_dir is None:
            self._cur_dir = VDirectory(arg_dir)
            self._top_dir = self._cur_dir
        else:
            if self._cur_dir.has_child(arg_dir):
                self._cur_dir = self._cur_dir.get_child(arg_dir)
            else:
                if arg_dir == "..":
                    self._cur_dir = self._cur_dir.parent
                else:
                    new_dir = VDirectory(arg_dir, self._cur_dir)
                    self._cur_dir = new_dir

    def run_command(self, command):
        cmd_funcs = {
            "cd": self._cmd_cd,
            "ls": self._cmd_ls,
        }

        parts = command.split(" ", 2)

        if parts[0] not in cmd_funcs:
            raise VFSError(f"Command '{parts[0]}' unknown.")

        if self.in_cmd:
            raise VFSError("Cannot process command output as a command.")

        if len(parts) == 1:
            parts.append(None)

        self._output_processor = cmd_funcs[parts[0]](parts[1])

    def process_command_line(self, line):
        if line[0] == "$":
            self._in_cmd = False
            self.run_command(line[1:].strip())
        else:
            if not self._in_cmd:
                raise VFSError("Cannot process output outside a command.")

            # if an output processor has been set, process the output, if not, skip
            if self._output_processor is not None:
                self._output_processor(line)
            else:
                pass


def recurse_filesystem(search_dir: VDirectory, max_size=0):
    child: VDirectory

    size = search_dir.size if search_dir.size <= max_size or max_size == 0 else 0

    for child in search_dir.children:
        if isinstance(child, VDirectory):
            size += recurse_filesystem(child, max_size)

    return size


def find_smallest(search_dir: VDirectory, min_size):
    # scenario 1: directory size is less than min_size, no further search, return None
    if search_dir.size < min_size:
        return None

    # scenario 2: directory is greater than or equal to min_size, search each child
    # directory, if child is greater than min_size, search that directory
    child: VFsObject
    smallest = search_dir.size

    for child in search_dir.children:
        if isinstance(child, VDirectory) and child.size >= min_size:
            size = find_smallest(child, min_size)

            if size is not None:
                if size < smallest:
                    smallest = size

    return smallest


def main():
    cmd = CommandLine()

    with open('input-data/day7-input.txt', 'r') as f:
        for f_line in f:
            cmd.process_command_line(f_line)

    size = 100000
    available_space = 70000000
    target_space = 30000000
    remaining_space = available_space - cmd.file_system.size
    space_to_free = target_space - (available_space - cmd.file_system.size)

    print(f"Total available space: {available_space:,}")
    print(f"Total space used: {cmd.file_system.size:,}")
    print(f"Remaining space: {remaining_space:,}")
    print(f"Space required: {target_space:,}")
    print(f"Space to free: {space_to_free:,}")

    print()
    print(f"Part 1: {recurse_filesystem(cmd.file_system, size):,}")

    smallest = find_smallest(cmd.file_system, space_to_free)

    print(f"Part 2: {smallest:,}")


if __name__ == '__main__':
    main()

