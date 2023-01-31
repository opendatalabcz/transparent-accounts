import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { format, subYears } from 'date-fns';
import TransactionsFilter from './TransactionsFilter';
import TransactionsTable from './TransactionsTable';
import { Transaction } from '../../types';
import { BsCloudDownload } from 'react-icons/bs';

interface Props {
  transactions: Array<Transaction>;
}

function Transactions({ transactions }: Props): JSX.Element {
  const [startDate, setStartDate] = useState<string>(format(subYears(new Date(), 1), 'yyyy-MM-d'));
  const [endDate, setEndDate] = useState<string>(format(new Date(), 'yyyy-MM-d'));
  const [type, setType] = useState<'' | 'INCOMING' | 'OUTGOING'>('');
  const [category, setCategory] = useState<'' | 'CARD' | 'ATM' | 'MESSAGE' | 'NO-MESSAGE'>('');
  const [query, setQuery] = useState<string>('');

  const downloadCSV = () => {
    // TODO
  };

  return (
    <Container fluid>
      <div className="d-flex justify-content-end">
        <Button variant="link" onClick={downloadCSV}>
          <BsCloudDownload className="d-inline-block align-text-top me-1" />
          uložit jako CSV
        </Button>
      </div>
      <div className="mt-2">
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
      <div className="mt-4">
        <TransactionsTable
          transactions={transactions}
          date={[startDate, endDate]}
          type={type}
          category={category}
          query={query}
        />
      </div>
    </Container>
  );
}

export default Transactions;
