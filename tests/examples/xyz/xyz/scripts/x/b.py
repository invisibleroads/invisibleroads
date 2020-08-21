from invisibleroads.scripts import Script


class XBScript(Script):

    def configure(self, argument_subparser):
        argument_subparser.add_argument('z')

    def run(self, args, argv):
        print('xb', args, argv)
