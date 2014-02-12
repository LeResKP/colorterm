import unittest
from colorterm.table import Table, Cell, Column, Display


class TestDisplay(unittest.TestCase):

    def test_init(self):
        d = Display()
        self.assertEqual(d._align, None)
        self.assertEqual(d._convert, None)

        d = Display(align='right', convert='something')
        self.assertEqual(d._align, 'right')
        self.assertEqual(d._convert, 'something')


class TestCell(unittest.TestCase):

    def test_init(self):
        # NOTE: Column is also tested here
        column = Column(name='col1')
        self.assertEqual(column.max_width, 4)
        cell = Cell(column, value='content')
        self.assertEqual(column.max_width, 7)
        self.assertEqual(cell.value, 'content')

        self.assertEqual(cell.align, 'left')
        self.assertEqual(cell.converts, [])

        column = Column(name='col1', convert='colconvert')
        cell = Cell(column, value='content', align='right',
                    convert='cellconvert')
        self.assertEqual(cell.align, 'right')
        self.assertEqual(cell.converts, ['colconvert', 'cellconvert'])

        column = Column(name='col1', convert='colconvert', align='right')
        cell = Cell(column, value='content', convert='cellconvert')
        self.assertEqual(cell.align, 'right')
        self.assertEqual(cell.converts, ['colconvert', 'cellconvert'])

    def test_display(self):
        column = Column(name='col1')
        cell = Cell(column, value='content')
        res = cell.display()
        self.assertEqual(res, 'content')

        column = Column(name='col1 very large')
        cell = Cell(column, value='content')
        res = cell.display()
        self.assertEqual(res, 'content        ')

        column = Column(name='col1 very large')
        cell = Cell(column, value='content', align='right')
        res = cell.display()
        self.assertEqual(res, '        content')

        column = Column(name='col1 very large',
                        convert=lambda x: "col%scol" % x)
        cell = Cell(column, value='content', align='right',
                    convert=lambda x: "cell%scell" % x)
        res = cell.display(lambda x: "extra%sextra" % x)
        self.assertEqual(res, 'cellcolextra        contentextracolcell')


class TestTable(unittest.TestCase):

    def test_init(self):
        table = Table('col1', 'col2')
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(len(table.rows[0]), 2)
        row1, row2 = table.rows[0]
        self.assertEqual(row1.value, 'col1')
        self.assertEqual(row2.value, 'col2')

        table = Table({'name': 'col1', 'align': 'right'}, 'col2')
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(len(table.rows[0]), 2)
        row1, row2 = table.rows[0]
        self.assertEqual(row1.value, 'col1')
        self.assertEqual(row2.value, 'col2')
        self.assertEqual(row1.colobj._align, 'right')
        self.assertEqual(row2.colobj._align, 'left')

        try:
            table = Table({'align': 'right'}, 'col2')
            assert(False)
        except Exception, e:
            self.assertEqual(str(e), 'Column name is not defined')

    def test_add_row(self):
        table = Table('col1', 'col2')
        table.add_row({'col1': {'value': 'cell1', 'align': 'right'},
                       'col2': 'cell2'})

        self.assertEqual(len(table.rows), 2)
        self.assertEqual(len(table.rows[0]), 2)
        self.assertEqual(len(table.rows[1]), 2)
        row1, row2 = table.rows[1]
        self.assertEqual(row1.value, 'cell1')
        self.assertEqual(row1._align, 'right')
        self.assertEqual(row2.value, 'cell2')
        self.assertEqual(row2._align, None)

    def test_display(self):
        table = Table('col1 large', 'col2', header_convert=lambda x: 'h%sh' % x)
        table.add_row({'col1 large': {'value': 'cell1', 'align': 'right'},
                       'col2': 'cell2'})
        res = table.display()
        expected = 'hcol1 largeh  hcol2 h\n     cell1  cell2'
        self.assertEqual(res, expected)

        table = Table('col1 large', 'col2',
                      header_convert=lambda x: 'h%sh' % x,
                      column_separator=' | ')
        table.add_row({'col1 large': {'value': 'cell1', 'align': 'right'},
                       'col2': 'cell2'})
        res = table.display()
        expected = 'hcol1 largeh | hcol2 h\n     cell1 | cell2'
        self.assertEqual(res, expected)
