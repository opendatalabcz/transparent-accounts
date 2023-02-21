import { Column } from 'react-table';
import { format } from 'date-fns';
import MoneyAmount from '../../features/format/MoneyAmount';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

export const transactionsColumns: Array<Column> = [
  {
    Header: 'Datum',
    accessor: 'date',
    Cell: ({ value }) => (
      <span className="text-nowrap">{format(new Date(value), 'dd.MM.yyyy')}</span>
    ),
    filter: 'date'
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
    Header: () => {
      return (
        <OverlayTrigger placement="bottom" overlay={<Tooltip>Variabilní symbol</Tooltip>}>
          <span>VS</span>
        </OverlayTrigger>
      );
    },
    accessor: 'variable_symbol'
  },
  {
    Header: () => {
      return (
        <OverlayTrigger placement="bottom" overlay={<Tooltip>Konstantní symbol</Tooltip>}>
          <span>KS</span>
        </OverlayTrigger>
      );
    },
    accessor: 'constant_symbol'
  },
  {
    Header: 'Poznámka',
    accessor: 'description'
  },
  {
    Header: () => {
      return (
        <OverlayTrigger placement="bottom" overlay={<Tooltip>Název společnosti získaný z IČO</Tooltip>}>
          <span>Společnost</span>
        </OverlayTrigger>
      );
    },
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
