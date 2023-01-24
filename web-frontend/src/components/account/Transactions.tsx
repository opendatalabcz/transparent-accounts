import { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import dayjs from 'dayjs'
import TransactionsFilter from './TransactionsFilter';
import TransactionTable from './TransactionTable';

function Transactions({ transactions })
{
    const [filteredTransactions, setFilteredTransactions] = useState(transactions);
    const [startDate, setStartDate] = useState(dayjs().subtract(1, 'year').format('YYYY-MM-DD'));
    const [endDate, setEndDate] = useState(dayjs().format('YYYY-MM-DD'));
    const [type, setType] = useState('ALL');
    const [category, setCategory] = useState('ALL');
    const [query, setQuery] = useState('')

    useEffect(() => {
        setFilteredTransactions(
            transactions
                .filter(t => t.date >= startDate && t.date <= endDate)
                .filter(t => type === 'ALL' || t.type === type)
                .filter(t => category === 'ALL' || t.category === category)
                .filter(t => t.description.includes(query))
        )
    }, [transactions, startDate, endDate, type, category, query])

    return (
        <div>
            <div className="mb-5">
                <TransactionsFilter {...{ startDate, setStartDate, endDate, setEndDate, type, setType, category, setCategory, query, setQuery }} />
            </div>
            <Container fluid>
                <TransactionTable transactions={filteredTransactions} />
            </Container>
        </div>
    )
}

export default Transactions;
