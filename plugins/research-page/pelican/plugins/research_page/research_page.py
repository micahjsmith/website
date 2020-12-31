import logging
import os.path
from copy import deepcopy
from functools import total_ordering
from typing import List

from pelican import signals
from pelican.generators import Generator

try:
    import citeproc
except ImportError:
    citeproc = None

logger = logging.getLogger(__name__)

_template_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    'data', 'templates')


DEFAULT_SETTINGS = {
    'BIBLIOGRAPHY_RESEARCH_TEMPLATE': _template_path,
    'BIBLIOGRAPHY_PATHS': ['bibliography'],
    'BIBLIOGRAPHY_EXCLUDES': [],
    'BIBLIOGRAPHY_EXTENSIONS': ['bib'],
    # 'BIBLIOGRAPHY_ORDER_BY': lambda ref: -ref.issued.year,  # TODO
}


@total_ordering
class AlwaysLessThan:
    def __lt__(self, other):
        return True


_lt = AlwaysLessThan()


class Reference:

    def __init__(self, ref: citeproc.source.Reference, meta: dict = None):
        self.fields = dict(ref)
        self.meta = {
            'key': ref.key,
            'type': ref.type,
        }
        if meta is not None:
            self.meta.update(meta)

    @property
    def sortkey(self):
        if 'issued' in self.fields:
            return self.fields['issued'].sort_key()
        else:
            return _lt


def read_references(base_path, path, context):
    """Parse content and metadata of csl files"""
    source_path = os.path.join(base_path, path)

    if not source_path.endswith('bib'):
        raise NotImplementedError

    references = []

    refsource = citeproc.source.bibtex.BibTeX(source_path, encoding='ascii')

    # process metadata
    metadata = {}
    _head, _tail = os.path.split(source_path)
    name, _ext = os.path.splitext(_tail)
    metadata['collection'] = name

    for key in refsource:
        ref = Reference(refsource[key], deepcopy(metadata))
        references.append(ref)

    return references


class BibliographyGenerator(Generator):

    def generate_context(self):
        bibliography: List[Reference] = []
        for file in self.get_files(
            self.settings['BIBLIOGRAPHY_PATHS'],
            exclude=self.settings['BIBLIOGRAPHY_EXCLUDES'],
            extensions=self.settings['BIBLIOGRAPHY_EXTENSIONS'],
        ):
            logger.debug(f'Reading references from {file}')
            try:
                new_references = read_references(
                    base_path=self.path, path=file, context=self.context)
            except Exception as e:
                logger.error(
                    'Could not process %s\n%s', file, e,
                    exc_info=self.settings.get('DEBUG', False))
                self._add_failed_source_path(file)
                continue

            logger.debug(f'Read {len(new_references)} references from {file}')
            bibliography.extend(new_references)

        self.bibliography = bibliography
        self._update_context(('bibliography', ))

    def generate_output(self, writer):
        pass


def update_settings(pelican):
    for key in DEFAULT_SETTINGS:
        pelican.settings.setdefault(key, DEFAULT_SETTINGS[key])
    if pelican.settings['BIBLIOGRAPHY_RESEARCH_TEMPLATE']:
        pelican.settings['THEME_TEMPLATES_OVERRIDES'].append(
            pelican.settings['BIBLIOGRAPHY_RESEARCH_TEMPLATE'])


def get_generators(pelican_object):
    return BibliographyGenerator


def register():
    signals.initialized.connect(update_settings)
    signals.get_generators.connect(get_generators)
