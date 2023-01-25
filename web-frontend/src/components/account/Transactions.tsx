import { useState } from 'react';
import { Container } from 'react-bootstrap';
import dayjs from 'dayjs';
import TransactionsFilter from './TransactionsFilter';
import TransactionTable from './TransactionTable';

function Transactions({ transactions }) {
  const [startDate, setStartDate] = useState(dayjs().subtract(1, 'month').format('YYYY-MM-DD'));
  const [endDate, setEndDate] = useState(dayjs().format('YYYY-MM-DD'));
  const [type, setType] = useState('');
  const [category, setCategory] = useState('');
  const [query, setQuery] = useState('');

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
        <TransactionTable
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
