import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard, { renderAppearances } from './AnalysisTableCard';
import { Appearance } from '../../types';

interface Props {
  data: Array<Appearance>;
}

function IdentifierTable({ data }: Props): JSX.Element {
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
      title={'Agregace odchozích transakcí podle IČO'}
      columns={columns}
      data={data}
    />
  );
}

export default IdentifierTable;
