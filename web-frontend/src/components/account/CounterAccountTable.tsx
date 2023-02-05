import { Column } from 'react-table';
import AnalysisTableCard, { renderAppearances } from './AnalysisTableCard';
import MoneyAmount from '../../features/format/MoneyAmount';
import { Appearance } from '../../types';

interface Props {
  data: Array<Appearance>
}

function IdentifierTable({ data }: Props): JSX.Element {
  const columns: Array<Column> = [
    {
      Header: 'Název protiúčtu',
      accessor: 'name'
    },
    {
      Header: 'Transakcí',
      accessor: 'transactionsCount'
    },
    {
      Header: 'Celková částka',
      accessor: 'totalAmount',
      Cell: ({ value }) => <MoneyAmount amount={value} currency="CZK" />
    },
    {
      Header: 'Jinde',
      accessor: 'appearances',
      Cell: renderAppearances
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
