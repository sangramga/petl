from __future__ import absolute_import, print_function, division, \
    unicode_literals


# standard library dependencies
import codecs
from ..compat import text_type, number_types, next


# internal dependencies
from ..util import RowContainer
from .sources import write_source_from_arg


def tohtml(table, source=None, caption=None, representation=text_type,
           lineterminator='\r\n'):
    """
    Write the table as HTML to a file. E.g.::

        >>> from petl import tohtml, look
        >>> look(table)
        +-------+-------+
        | 'foo' | 'bar' |
        +=======+=======+
        | 'a'   | 1     |
        +-------+-------+
        | 'b'   | 2     |
        +-------+-------+
        | 'c'   | 2     |
        +-------+-------+

        >>> tohtml(table, 'test.html')

    .. versionadded:: 0.12

    .. versionchanged:: 0.17.1

    Added support for ``caption`` keyword argument to provide table caption
    in output.

    """

    source = write_source_from_arg(source)
    with source.open_('w') as f:
        it = iter(table)
        flds = next(it)
        _write_begin(f, flds, lineterminator, caption)
        for row in it:
            _write_row(f, row, lineterminator, representation)
        _write_end(f, lineterminator)


def teehtml(table, source=None, caption=None, representation=text_type,
            lineterminator='\r\n'):
    """
    Return a table that writes rows to an HTML file as they are iterated over.

    .. versionadded:: 0.25

    """

    return TeeHTMLContainer(table, source=source, caption=caption,
                            representation=representation,
                            lineterminator=lineterminator)


class TeeHTMLContainer(RowContainer):

    def __init__(self, table, source=None, caption=None,
                 representation=text_type, lineterminator='\r\n'):
        self.table = table
        self.source = source
        self.caption = caption
        self.representation = representation
        self.lineterminator = lineterminator

    def __iter__(self):
        source = write_source_from_arg(self.source)
        lineterminator = self.lineterminator
        caption = self.caption
        representation = self.representation
        with source.open_('w') as f:
            it = iter(self.table)
            flds = next(it)
            _write_begin(f, flds, lineterminator, caption)
            yield flds
            for row in it:
                _write_row(f, row, lineterminator, representation)
                yield row
            _write_end(f, lineterminator)


def _write_begin(f, flds, lineterminator, caption):
    f.write("<table class='petl'>" + lineterminator)
    if caption is not None:
        f.write(('<caption>%s</caption>' % caption) + lineterminator)
    f.write('<thead>' + lineterminator)
    f.write('<tr>' + lineterminator)
    for h in flds:
        f.write(('<th>%s</th>' % h) + lineterminator)
    f.write('</tr>' + lineterminator)
    f.write('</thead>' + lineterminator)
    f.write('<tbody>' + lineterminator)


def _write_row(f, row, lineterminator, representation):
    f.write('<tr>' + lineterminator)
    for v in row:
        r = representation(v)
        if isinstance(v, number_types) and not isinstance(v, bool):
            f.write(("<td style='text-align: right'>%s</td>" % r)
                    + lineterminator)
        else:
            f.write(('<td>%s</td>' % r) + lineterminator)
    f.write('</tr>' + lineterminator)


def _write_end(f, lineterminator):
    f.write('</tbody>' + lineterminator)
    f.write('</table>' + lineterminator)


def touhtml(table, source=None, caption=None, encoding='utf-8',
            representation=text_type, lineterminator='\r\n'):
    """
    Write the table as Unicode HTML to a file.

    .. versionadded:: 0.19
    """

    source = write_source_from_arg(source)
    with source.open_('wb') as f:
        f = codecs.getwriter(encoding)(f)
        it = iter(table)
        flds = next(it)
        _write_begin_unicode(f, flds, lineterminator, caption)
        for row in it:
            _write_row_unicode(f, row, lineterminator, representation)
        _write_end_unicode(f, lineterminator)


def teeuhtml(table, source=None, caption=None,
             encoding='utf-8', representation=text_type, lineterminator='\r\n'):
    """
    Return a table that writes rows to a Unicode HTML file as they are iterated
    over.

    .. versionadded:: 0.25

    """

    return TeeUHTMLContainer(table, source=source, caption=caption,
                             encoding=encoding, representation=representation,
                             lineterminator=lineterminator)


class TeeUHTMLContainer(RowContainer):

    def __init__(self, table, source=None, caption=None,
                 encoding='utf-8', representation=text_type,
                 lineterminator='\r\n'):
        self.table = table
        self.source = source
        self.caption = caption
        self.encoding = encoding
        self.representation = representation
        self.lineterminator = lineterminator

    def __iter__(self):
        source = write_source_from_arg(self.source)
        lineterminator = self.lineterminator
        caption = self.caption
        representation = self.representation
        with source.open_('wb') as f:
            f = codecs.getwriter(self.encoding)(f)
            it = iter(self.table)
            flds = next(it)
            _write_begin_unicode(f, flds, lineterminator, caption)
            yield flds
            for row in it:
                _write_row_unicode(f, row, lineterminator, representation)
                yield row
            _write_end_unicode(f, lineterminator)


def _write_begin_unicode(f, flds, lineterminator, caption):
    f.write("<table class='petl'>" + lineterminator)
    if caption is not None:
        f.write(('<caption>%s</caption>' % caption) + lineterminator)
    f.write('<thead>' + lineterminator)
    f.write('<tr>' + lineterminator)
    for h in flds:
        f.write(('<th>%s</th>' % h) + lineterminator)
    f.write('</tr>' + lineterminator)
    f.write('</thead>' + lineterminator)
    f.write('<tbody>' + lineterminator)


def _write_row_unicode(f, row, lineterminator, representation):
    f.write('<tr>' + lineterminator)
    for v in row:
        r = representation(v)
        if isinstance(v, number_types) \
                and not isinstance(v, bool):
            f.write(("<td style='text-align: right'>%s</td>" % r)
                    + lineterminator)
        else:
            f.write(('<td>%s</td>' % r) + lineterminator)
    f.write('</tr>' + lineterminator)


def _write_end_unicode(f, lineterminator):
    f.write('</tbody>' + lineterminator)
    f.write('</table>' + lineterminator)
