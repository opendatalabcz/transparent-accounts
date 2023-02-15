import { Column } from 'react-table';
import MoneyAmount from '../../features/format/MoneyAmount';
import AnalysisTableCard from './AnalysisTableCard';
import { Account, TransactionsAggregation } from '../../types';
import { IdentifierOccurrences } from './Occurrences';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

interface Props {
  account: Account;
  data: Array<TransactionsAggregation>;
}

function IdentifierTable({ account, data }: Props): JSX.Element {
  const columns: Array<Column> = [
    {
      Header: () => {
        return (
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Název společnosti</Tooltip>}>
            <span>Název společnosti</span>
          </OverlayTrigger>
        );
      },
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
      Header: () => {
        return (
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Počet transakcí</Tooltip>}>
            <span>Počet</span>
          </OverlayTrigger>
        );
      },
      accessor: 'transactionsCount'
    },
    {
      Header: () => {
        return (
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Celková částka</Tooltip>}>
            <span>Celkem</span>
          </OverlayTrigger>
        );
      },
      accessor: 'totalAmount',
      Cell: ({ row }) => (
        <MoneyAmount amount={row.original.totalAmount} currency={row.original.currency} />
      )
    },
    {
      Header: () => {
        return (
          <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip>Počet výskytů u jiných transparentních účtů</Tooltip>}>
            <span>Výskyty</span>
          </OverlayTrigger>
        );
      },
      id: 'occurrences',
      canSort: false,
      Cell: ({ row }) => (
        <IdentifierOccurrences account={account} identifier={row.original.identifier} />
      )
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace odchozích transakcí podle názvu společnosti'}
      description={
        'Agregace odchozích transakcí podle IČO. Název společnosti je získán z Ministerstva financí ČR.'
      }
      columns={columns}
      data={data}
    />
  );
}

export default IdentifierTable;
