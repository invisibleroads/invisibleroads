import json
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from collections import defaultdict
from stevedore.extension import ExtensionManager


class Script(ABC):

    priority = 100

    @abstractmethod
    def configure(self, argument_subparser):
        pass

    @abstractmethod
    def run(self, args, argv):
        pass


class ConfigurableScript(Script):

    def configure(self, argument_subparser):
        argument_names = get_argument_names(argument_subparser)
        if 'configuration_path' not in argument_names:
            argument_subparser.add_argument('configuration_path')


def launch(argv=sys.argv):
    launch_script('invisibleroads', argv)


def launch_script(script_name, argv):
    argument_parser = ArgumentParser(script_name)
    scripts_by_name = get_scripts_by_name(script_name)
    parser_by_name = configure_parser(argument_parser, scripts_by_name)
    run_scripts(argument_parser, parser_by_name, scripts_by_name, argv)


def get_scripts_by_name(extension_namespace):
    scripts_by_name = defaultdict(list)

    def handle_load_failure(manager, entrypoint, exception):
        print(entrypoint, exception)

    extension_manager = ExtensionManager(
        extension_namespace,
        invoke_on_load=True,
        on_load_failure_callback=handle_load_failure)
    for name, extension in zip(
            extension_manager.names(), extension_manager.extensions):
        scripts_by_name[name].append(extension.obj)
    for name, scripts in scripts_by_name.items():
        scripts_by_name[name] = sorted(scripts, key=lambda x: x.priority)
    return dict(scripts_by_name)


def configure_parser(argument_parser, scripts_by_name):
    scripts_by_command_name_by_target_name = defaultdict(dict)
    for name, scripts in scripts_by_name.items():
        try:
            target_name, command_name = name.split('.')
        except ValueError:
            target_name = ''
            command_name = name
        scripts_by_command_name_by_target_name[target_name][
            command_name] = scripts
    # if (is_target_expected(scripts_by_command_name_by_target_name)):
    argument_subparsers = argument_parser.add_subparsers(dest='target')
    # else:
    # argument_subparsers = argument_parser.add_subparsers(dest='command')

    target_parser_by_name = {}
    for (
        target_name, scripts_by_command_name,
    ) in scripts_by_command_name_by_target_name.items():
        if target_name:
            target_parser = argument_subparsers.add_parser(target_name)
            target_parser_by_name[target_name] = target_parser
            target_subparsers = target_parser.add_subparsers(dest='command')
        for command_name, scripts in scripts_by_command_name.items():
            if target_name:
                subparsers = target_subparsers
            else:
                subparsers = argument_subparsers
            command_parser = subparsers.add_parser(command_name)
            for script in scripts:
                script.configure(command_parser)
    return target_parser_by_name


def is_target_expected(scripts_by_name):
    target_count = sum(1 for name, _ in scripts_by_name.items() if name != '')
    return target_count > 0


def run_scripts(argument_parser, parser_by_name, scripts_by_name, argv):
    known_args, extra_argv = argument_parser.parse_known_args(argv[1:])
    target_name = getattr(known_args, 'target', None) or ''
    command_name = getattr(known_args, 'command', None) or ''
    try:
        scripts = scripts_by_name[target_name + '.' + command_name]
    except KeyError:
        try:
            scripts = scripts_by_name[target_name]
        except KeyError:
            scripts = []
    if not scripts:
        if not target_name:
            argument_parser.print_help()
        elif not command_name:
            parser_by_name[target_name].print_help()
    for script in scripts:
        d = script.run(known_args, extra_argv)
        if not d:
            continue
        print(json.dumps(d))


def get_argument_names(argument_subparser):
    return [_.dest for _ in argument_subparser._actions]
