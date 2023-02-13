import { Column } from 'react-table';
import AnalysisTableCard from './AnalysisTableCard';
import MoneyAmount from '../../features/format/MoneyAmount';
import { Account, TransactionsAggregation } from '../../types';
import { CounterAccountOccurrences } from './Occurrences';

interface Props {
  account: Account;
  data: Array<TransactionsAggregation>;
}

function IdentifierTable({ account, data }: Props): JSX.Element {
  const columns: Array<Column> = [
    {
      Header: 'Protiúčet',
      accessor: 'name'
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
        <CounterAccountOccurrences account={account} counterAccount={row.original.name} />
      )
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace příchozích transakcí podle protiúčtu'}
      columns={columns}
      data={data}
    />
  );
}

export default IdentifierTable;
