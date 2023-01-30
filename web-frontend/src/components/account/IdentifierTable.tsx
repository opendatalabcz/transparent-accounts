import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard, { renderAppearances } from './AnalysisTableCard';
import { Appearance } from '../../types';

interface Props {
  data: Array<Appearance>
}

function IdentifierTable({ data }: Props): JSX.Element {
  const columns: Array<Column> = [
    {
      Header: 'IČO',
      accessor: 'name',
      Cell: ({ value }) => (
        <a target="_blank" rel="noreferrer" href={`https://rejstrik-firem.kurzy.cz/${value}`}>
          {value}
        </a>
      )
    },
    {
      Header: 'Výskyty',
      accessor: 'appearances',
      Cell: renderAppearances
    },
    {
      Header: 'Počet transakcí',
      accessor: 'transactionsCount'
    },
    {
      Header: 'Celková částka',
      accessor: 'totalAmount',
      Cell: ({ value }) => <MoneyAmount amount={value} currency="CZK" />
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
