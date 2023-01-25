import { useState } from 'react';
import { Container } from 'react-bootstrap';
import dayjs from 'dayjs';
import TransactionsFilter from './TransactionsFilter';
import TransactionsTable from './TransactionsTable';

function Transactions({ transactions }) {
  const [startDate, setStartDate] = useState(dayjs().subtract(1, 'year').format('YYYY-MM-DD'));
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
