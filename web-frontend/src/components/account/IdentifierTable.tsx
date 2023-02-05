import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard from './AnalysisTableCard';
import { Account, TransactionsAggregation } from '../../types';
import { IdentifierOccurrences } from './Occurrences';

interface Props {
  account: Account;
  data: Array<TransactionsAggregation>;
}

function IdentifierTable({ account, data }: Props): JSX.Element {
  const columns: Array<Column> = [
    {
      Header: 'IČO',
      accessor: 'name',
      Cell: ({ row }) => (
        <a
          target="_blank"
          rel="noreferrer"
          href={`https://rejstrik-firem.kurzy.cz/${row.original.identifier}`}>
          {row.original.name}
        </a>
      )
    },
    {
      Header: 'Transakcí',
      accessor: 'transactionsCount'
    },
    {
      Header: 'Celková částka',
      accessor: 'totalAmount',
      Cell: ({ row }) => (
        <MoneyAmount amount={row.original.totalAmount} currency={row.original.currency} />
      )
    },
    {
      Header: 'Jinde',
      id: 'occurrences',
      canSort: false,
      Cell: ({ row }) => (
        <IdentifierOccurrences account={account} identifier={row.original.identifier} />
      )
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace odchozích transakcí podle IČO'}
      columns={columns}
      data={data}
    />
  );
}

export default IdentifierTable;
