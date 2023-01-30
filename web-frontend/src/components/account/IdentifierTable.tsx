import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard from './AnalysisTableCard';

function IdentifierTable(): JSX.Element {
  const analysisColumns: Array<Column> = [
    {
      Header: 'IČO',
      accessor: 'identifier'
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
      identifier: '12345678',
      appearances: 4,
      count: 1,
      amount: -65434
    },
    {
      identifier: '87654321',
      appearances: 0,
      count: 6,
      amount: -25434
    },
    {
      identifier: '01234567',
      appearances: 0,
      count: 1,
      amount: -100
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace odchozích transakcí podle IČO'}
      columns={analysisColumns}
      data={example}
    />
  );
}

export default IdentifierTable;
