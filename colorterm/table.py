from colorterm import ColorTerm

colorterm = ColorTerm()


class Display(object):
    _align = None
    _convert = None

    def __init__(self, **kw):
        for param in ['align', 'convert']:
            if param in kw:
                setattr(self, '_%s' % param, kw[param])


class Cell(Display):

    def __init__(self, colobj, **kw):
        super(Cell, self).__init__(**kw)
        self.colobj = colobj
        self.value = unicode(kw['value'] if kw['value'] is not None else '')
        self.colobj.set_max_width(len(self.value))

    @property
    def align(self):
        return self._align or self.colobj._align

    @property
    def converts(self):
        return filter(bool, [self.colobj._convert, self._convert])

    def display(self, convert=None):
        width = self.colobj.max_width
        if self.align == 'right':
            value = self.value.rjust(width)
        elif self.align == 'left':
            value = self.value.ljust(width)
        else:
            raise Exception('align %s not supported' % self.align)
        if convert:
            value = convert(value)
        for convert in self.converts:
            value = convert(value)
        return value


class Column(Display):
    _align = 'left'

    def __init__(self, **kw):
        super(Column, self).__init__(**kw)
        self.name = kw['name']
        self.max_width = len(self.name)

    def set_max_width(self, width):
        self.max_width = max(self.max_width, width)


class Table(object):
    column_separator = '  '
    header_convert = staticmethod(colorterm.underline)

    def __init__(self, *colums, **kw):
        self.columns = []
        self.rows = []
        for param in ['column_separator', 'header_convert']:
            if param in kw:
                setattr(self, param, kw[param])

        # Initialize the columns and the header rows
        lis = []
        for col in colums:
            if not isinstance(col, dict):
                col = {'name': col}
            if 'name' not in col:
                raise Exception('Column name is not defined')
            colobj = Column(**col)
            self.columns += [colobj]
            lis += [Cell(colobj, value=colobj.name)]

        self.rows += [lis]

    def add_row(self, dic, convert=None):
        lis = []
        for colobj in self.columns:
            value = dic.get(colobj.name)
            if not isinstance(value, dict):
                value = {'value': value}
            if convert and convert not in value:
                value['convert'] = convert
            cobj = Cell(colobj, **value)
            lis += [cobj]
        self.rows += [lis]

    def display(self):
        s = []
        for index, row in enumerate(self.rows):
            convert = None
            if index == 0:
                convert = self.header_convert
            lis = []
            for r in row:
                lis += [r.display(convert)]
            s += [self.column_separator.join(lis)]
        return '\n'.join(s)


if __name__ == '__main__':

    t = Table({
        'name': 'ID',
        'align': 'right',
        'convert': colorterm.red,
    }, 'Project', 'Description', column_separator=' | ')
    for (i, p, d) in [(1, 'a', 'A'), (2, 'b', 'B'), (3, 'c', 'C')]:
        dic = {
            'ID': i,
            'Project': p,
            'Description': d,
        }
        t.add_row(dic)

    print t.display()
