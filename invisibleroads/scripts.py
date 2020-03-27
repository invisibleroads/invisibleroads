import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from collections import defaultdict
from invisibleroads_macros_log import format_summary
from stevedore.extension import ExtensionManager


class Script(ABC):

    priority = 100

    @abstractmethod
    def configure(self, argument_subparser):
        pass

    @abstractmethod
    def run(self, args):
        pass


class ConfigurableScript(Script):

    def configure(self, argument_subparser):
        argument_names = get_argument_names(argument_subparser)
        if 'configuration_path' not in argument_names:
            argument_subparser.add_argument('configuration_path')


def launch(argv=sys.argv):
    argument_parser = ArgumentParser('invisibleroads', add_help=False)
    argument_subparsers = argument_parser.add_subparsers(dest='command')
    scripts_by_name = get_scripts_by_name('invisibleroads')
    configure_subparsers(argument_subparsers, scripts_by_name)
    args = argument_parser.parse_args(argv[1:])
    run_scripts(scripts_by_name, args)


def get_scripts_by_name(extension_namespace):
    scripts_by_name = defaultdict(list)
    extension_manager = ExtensionManager(
        extension_namespace, invoke_on_load=True)
    for name, extension in zip(
            extension_manager.names(), extension_manager.extensions):
        scripts_by_name[name].append(extension.obj)
    for name, scripts in scripts_by_name.items():
        scripts_by_name[name] = sorted(scripts, key=lambda x: x.priority)
    return scripts_by_name


def configure_subparsers(argument_subparsers, scripts_by_name):
    for name, scripts in scripts_by_name.items():
        argument_subparser = argument_subparsers.add_parser(
            name, add_help=False)
        for script in scripts:
            script.configure(argument_subparser)


def run_scripts(scripts_by_name, args, target_name=None):
    if not target_name:
        target_name = args.command
    for script in scripts_by_name[target_name]:
        d = script.run(args)
        if not d:
            continue
        print(format_summary(d))


def get_argument_names(argument_subparser):
    return [_.dest for _ in argument_subparser._actions]
