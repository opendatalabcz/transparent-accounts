import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard from './AnalysisTableCard';

function IdentifierTable(): JSX.Element {
  const analysisColumns: Array<Column> = [
    {
      Header: 'Název protiúčtu',
      accessor: 'counterAccount'
    },
    {
      Header: 'Výskyty u jiných účtů',
      accessor: 'appearances'
    },
    {
      Header: 'Počet transakcí',
      accessor: 'count'
    },
    {
      Header: 'Celková částka',
      accessor: 'amount',
      Cell: ({ value }) => <MoneyAmount amount={value} currency="CZK" />
    }
  ];

  const example = [
    {
      counterAccount: 'Jan Novák',
      appearances: 0,
      count: 2,
      amount: 1250000
    },
    {
      counterAccount: 'Jakub Janeček',
      appearances: 1,
      count: 3,
      amount: 25434
    },
    {
      counterAccount: 'Jan Černý',
      appearances: 0,
      count: 1,
      amount: 233
    },
    {
      counterAccount: 'Jakub Cabrnoch',
      appearances: 4,
      count: 4,
      amount: 0.04
    },
    {
      counterAccount: 'Natálie Kmochová',
      appearances: 4,
      count: 1,
      amount: 0.04
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace příchozích transakcí podle protiúčtu'}
      columns={analysisColumns}
      data={example}
    />
  );
}

export default IdentifierTable;
