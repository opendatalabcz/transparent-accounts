import { useState } from 'react';
import { Container } from 'react-bootstrap';
import TransactionsFilter from './TransactionsFilter';
import TransactionsTable from './TransactionsTable';
import { Transaction } from '../../types';
import { downloadBlob, transactionToCSV } from '../../utils/csvDownload';

interface Props {
  transactions: Array<Transaction>;
}

function Transactions({ transactions }: Props): JSX.Element {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [type, setType] = useState<'' | 'INCOMING' | 'OUTGOING'>('');
  const [category, setCategory] = useState<'' | 'CARD' | 'ATM' | 'MESSAGE' | 'NO-MESSAGE'>('');
  const [query, setQuery] = useState<string>('');

  const downloadCSV = () => {
    // Prepare the CSV file
    const csv = transactionToCSV(transactions);
    // Download the CSV file
    downloadBlob(csv, 'transakce.csv', 'text/csv;charset=utf-8;');
  };

  return (
    <Container fluid>
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
            setQuery,
            downloadCSV
          }}
        />
      </div>
      <Container fluid className="mt-4">
        <TransactionsTable
          transactions={transactions}
          date={[startDate, endDate]}
          type={type}
          category={category}
          query={query}
        />
      </Container>
    </Container>
  );
}

export default Transactions;
