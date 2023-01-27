import { useState } from 'react';
import { Container } from 'react-bootstrap';
import dayjs from 'dayjs';
import TransactionsFilter from './TransactionsFilter';
import TransactionsTable from './TransactionsTable';
import { Transaction } from '../../types';

interface Props {
  transactions: Array<Transaction>
}

function Transactions({ transactions }: Props): JSX.Element {
  const [startDate, setStartDate] = useState<string>(dayjs().subtract(1, 'year').format('YYYY-MM-DD'));
  const [endDate, setEndDate] = useState<string>(dayjs().format('YYYY-MM-DD'));
  const [type, setType] = useState<'' | 'INCOMING' | 'OUTGOING'>('');
  const [category, setCategory] = useState<'' | 'MESSAGES' | 'NO-MESSAGES'>('');
  const [query, setQuery] = useState<string>('');

  return (
    <div>
      <div className="mb-5">
        <TransactionsFilter
          {...{
            startDate,
            setStartDate,
            endDate,
            setEndDate,
            type,
            setType,
            category,
            setCategory,
            query,
            setQuery
          }}
        />
      </div>
      <Container fluid>
        <TransactionsTable
          transactions={transactions}
          date={[startDate, endDate]}
          type={type}
          category={category}
          query={query}
        />
      </Container>
    </div>
  );
}

export default Transactions;
