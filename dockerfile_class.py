class DockerfileClass:
    _add_commands = []
    _copy_commands = []
    _run_commands = []
    _entry_point = None
    _base_image = ""
    _command_order = []
    _exposed_ports = []
    _apt_packages_list = []
    _update_apt_get = False

    def __init__(self):
        pass

    def base_image(self, base_image_tag):
        self._base_image = base_image_tag
        return self

    def apt_get_update(self):
        self._update_apt_get = True
        return self

    def apt_install(self, package_name):
        self._update_apt_get = True
        self._apt_packages_list.append(package_name)
        return self

    def add_command(self, from_path, to_path):
        self._command_order.append(('a', len(self._add_commands)))
        self._add_commands.append((from_path, to_path))
        return self

    def copy_command(self, from_path, to_path):
        self._command_order.append(('c', len(self._copy_commands)))
        self._copy_commands.append((from_path, to_path))
        return self

    def expose_command(self, port_number):
        self._command_order.append(('e', len(self._exposed_ports)))
        self._exposed_ports.append(port_number)
        return self

    def run_command(self, command):
        self._command_order.append(('r', len(self._run_commands)))
        self._run_commands.append(command)
        return self

    def entrypoint(self, entrypoint_cmd, *args):
        self._entry_point = (entrypoint_cmd, args[0], args[1], args[2])
        return self

    def write(self):
        output_file = open('Dockerfile', 'w')
        output_file.write("FROM {}\n\n".format(self._base_image))

        if self._update_apt_get:
            apt_install_command = "RUN apt-get update"
            if len(self._apt_packages_list) > 0:
                apt_install_command += ' && apt-get install -y \\\n'
                for item in self._apt_packages_list:
                    apt_install_command += "\t{} \\\n".format(item)

                apt_install_command = apt_install_command[0:-2]+'\n\n'
                output_file.write(apt_install_command)

        for pair in self._command_order:
            self._write_command(output_file, pair)

        output_file.write("ENTRYPOINT [\"{}\", \"{}\", \"{}\", \"{}\"]\n".format(*self._entry_point))
        output_file.close()

    def _write_command(self, out_file, pair):
        if pair[0] == 'a':
            out_file.write("ADD {} {}\n".format(*self._add_commands[pair[1]]))
        elif pair[0] == 'c':
            out_file.write("COPY {} {}\n".format(*self._copy_commands[pair[1]]))
        elif pair[0] == 'e':
            out_file.write("EXPOSE {}\n".format(*self._exposed_ports[pair[1]]))
        elif pair[0] == 'r':
            out_file.write("RUN {}\n".format(self._run_commands[pair[1]]))
