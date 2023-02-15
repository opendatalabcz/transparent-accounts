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
    accessor: 'type_detail',
    Cell: ({ value }) => <span className="text-nowrap">{value}</span>
  },
  {
    Header: 'Protiúčet',
    accessor: 'counter_account',
    Cell: ({ value }) => <span className="text-nowrap">{value}</span>
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
    Header: 'Poznámka',
    accessor: 'description'
  },
  {
    Header: 'IČO',
    accessor: 'ca_name',
    Cell: ({ row }) => (
      <a
        target="_blank"
        rel="noreferrer"
        href={`https://rejstrik-firem.kurzy.cz/${row.original.ca_identifier}`}>
        {row.original.ca_name}
      </a>
    )
  },
  {
    Header: 'Kategorie',
    accessor: 'category',
    filter: 'category'
  }
];
