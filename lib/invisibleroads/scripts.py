from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from collections import defaultdict
from invisibleroads_macros.log import format_nested_dictionary
from itertools import izip
from six import add_metaclass
from stevedore.extension import ExtensionManager


@add_metaclass(ABCMeta)
class Script(object):

    priority = 100

    @abstractmethod
    def configure(self, argument_subparser):
        pass

    @abstractmethod
    def run(self, args):
        pass


@add_metaclass(ABCMeta)
class ConfigurableScript(Script):

    def configure(self, argument_subparser):
        if not argument_subparser.has_argument('configuration_path'):
            argument_subparser.add_argument('configuration_path')

    @abstractmethod
    def run(self, args):
        pass


class ReflectiveArgumentParser(ArgumentParser):

    def has_argument(self, dest):
        for action in self._actions:
            if action.dest == dest:
                return True
        return False


def get_scripts_by_name(namespace):
    scripts_by_name = defaultdict(list)
    extension_manager = ExtensionManager(namespace, invoke_on_load=True)
    for name, extension in izip(
            extension_manager.names(), extension_manager.extensions):
        scripts_by_name[name].append(extension.obj)
    for name, scripts in scripts_by_name.iteritems():
        scripts_by_name[name] = sorted(scripts, key=lambda x: x.priority)
    return scripts_by_name


def configure_subparsers(argument_subparsers, scripts_by_name):
    for name, scripts in scripts_by_name.iteritems():
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
        print(format_nested_dictionary(d))
