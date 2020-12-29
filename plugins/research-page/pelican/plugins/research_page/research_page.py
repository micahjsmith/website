from pelican import signals
from pelican.generators import Generator
from pelican.readers import BaseReader


class CslReader(BaseReader):
    pass


class ReferenceGenerator(Generator):

    def generate_context(self):
        pass

    def generate_output(self, writer):
        pass


def add_reader(readers):
    if CslReader.enabled:
        for ext in CslReader.file_extensions:
            readers.reader_classes[ext] = CslReader


def get_generators(pelican_object):
    # define a new generator here if you need to
    return ReferenceGenerator

def register():
    signals.readers_init.connect(add_reader)
    signals.get_generators.connect(get_generators)
