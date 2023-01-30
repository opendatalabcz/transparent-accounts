import { useMemo } from 'react';
import { Container } from 'react-bootstrap';
import AnalysisCard, { AnalysisCardProps } from './AnalysisCard';
import { analyse } from '../../services/analysis';
import MoneyAmount from '../../features/format/MoneyAmount';
import { Analysis as AnalysisType, Transaction } from '../../types';
import IdentifierTable from './IdentifierTable';
import CounterAccountTable from './CounterAccountTable';
import ChartBalance from './ChartBalance';
import ChartTransactions from './ChartTransactions';

interface Props {
  transactions: Array<Transaction>;
  balance: number | null;
  currency: string | null;
}

function Analysis({ transactions, balance, currency }: Props): JSX.Element {
  // Analyse transactions
  const analysis: AnalysisType = useMemo(
    () => analyse(transactions, balance, currency),
    [transactions, balance, currency]
  );

  // Listing of shown analysis cards
  const metrics = useMemo<Array<AnalysisCardProps>>(
    () => [
      {
        name: 'Počet transakcí',
        value: analysis.transactionsCount,
        render: (value) => (value !== null ? <span>{value.toLocaleString('cs-CZ')}</span> : null)
      },
      {
        name: 'Počet příchozích transakcí',
        value: analysis.incomingCount,
        render: (value) => (value !== null ? <span>{value.toLocaleString('cs-CZ')}</span> : null)
      },
      {
        name: 'Počet odchozích transakcí',
        value: analysis.outgoingCount,
        render: (value) => (value !== null ? <span>{value.toLocaleString('cs-CZ')}</span> : null)
      },
      {
        name: 'Zůstatek',
        value: analysis.balance,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Suma příjmů',
        value: analysis.incomingAmount,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Suma výdajů',
        value: analysis.outgoingAmount,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Průměrná výše příchozí transakce',
        value: analysis.incomingAverage,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Průměrná výše odchozí transakce',
        value: analysis.outgoingAverage,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Medián výše příchozí transakce',
        value: analysis.incomingMedian,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Medián výše odchozí transakce',
        value: analysis.outgoingMedian,
        render: (value) => <MoneyAmount amount={value} currency={analysis.currency} />
      },
      {
        name: 'Úroveň transparentnosti účtu',
        value: analysis.transparency,
        description: 'Počítá se jako',
        render: (value) => (value != null ? <span>{Math.round(value * 100)} %</span> : null)
      },
      {
        name: 'Uvedená poznámka',
        value: analysis.noted,
        description: 'V kolika procentech odchozích transakcí je uvedena jakákoliv poznámka.',
        render: (value) => (value != null ? <span>{Math.round(value * 100)} %</span> : null)
      }
    ],
    [analysis]
  );

  return (
    <Container className="analysis">
      <div className="row">
        {metrics.map(
          (metric: AnalysisCardProps): JSX.Element => (
            <div key={metric.name} className="col-lg-3 col-md-4 col-sm-6 px-1 pb-2">
              <AnalysisCard metrics={metric} />
            </div>
          )
        )}
      </div>
      <div className="row">
        <div className="col-lg-6 col-12 px-1 pb-2">
          <IdentifierTable data={analysis.identifiers}/>
        </div>
        <div className="col-lg-6 col-12 px-1 pb-2">
          <CounterAccountTable data={analysis.counterAccounts}/>
        </div>
      </div>
      <div className="row">
        <div className="col-lg-6 col-12 px-1 pb-2">
          <ChartBalance data={[]}/>
        </div>
        <div className="col-lg-6 col-12 px-1 pb-2">
          <ChartTransactions data={[]} />
        </div>
      </div>
    </Container>
  );
}

export default Analysis;
