import { Column } from 'react-table';
import AnalysisTableCard from './AnalysisTableCard';
import MoneyAmount from '../../features/format/MoneyAmount';
import { Account, TransactionsAggregation } from '../../types';
import { CounterAccountOccurrences } from './Occurrences';
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
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Název protiúčtu</Tooltip>}>
            <span>Protiúčet</span>
          </OverlayTrigger>
        );
      },
      accessor: 'name'
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
        <CounterAccountOccurrences account={account} counterAccount={row.original.name} />
      )
    }
  ];

  return (
    <AnalysisTableCard
      title={'Agregace příchozích transakcí podle protiúčtu'}
      description={
        'Agregace příchozích transakcí podle uvedného protiúčtu. Nalezené výskyty u jiných účtů jsou pouze orientační, protože název protiúčtu nemusí být unikátní.'
      }
      columns={columns}
      data={data}
    />
  );
}

export default IdentifierTable;
