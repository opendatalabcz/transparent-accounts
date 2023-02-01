import { Column } from 'react-table';
import { format } from 'date-fns';
import MoneyAmount from '../../features/format/MoneyAmount';

export const transactionsColumns: Array<Column> = [
  {
    Header: 'Datum',
    accessor: 'date',
    Cell: ({ value }) => (
      <span className="text-nowrap">{format(new Date(value), 'dd.MM.yyyy')}</span>
    ),
    filter: 'between'
  },
  {
    Header: 'Částka',
    accessor: 'amount',
    Cell: ({ value }) => <MoneyAmount amount={value} currency="CZK" />,
    sortDescFirst: true,
    sortType: 'basic'
  },
  {
    id: 'type',
    accessor: 'type'
  },
  {
    Header: 'Typ',
    Cell: ({ value }) => <span className="text-nowrap">{value}</span>,
    accessor: 'type_detail'
  },
  {
    Header: 'Protiúčet',
    Cell: ({ value }) => <span className="text-nowrap">{value}</span>,
    accessor: 'counter_account'
  },
  {
    Header: 'VS',
    accessor: 'variable_symbol'
  },
  {
    Header: 'KS',
    accessor: 'constant_symbol'
  },
  {
    Header: 'SS',
    accessor: 'specific_symbol'
  },
  {
    Header: 'Poznámka',
    accessor: 'description'
  },
  {
    Header: 'IČO',
    accessor: 'identifier'
  },
  {
    Header: 'Kategorie',
    accessor: 'category',
    filter: 'category'
  }
];
