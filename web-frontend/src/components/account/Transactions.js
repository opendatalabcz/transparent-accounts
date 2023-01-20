import { Container } from 'react-bootstrap';
import TransactionsFilter from './TransactionsFilter';
import TransactionTable from './TransactionTable';

function Transactions({ transactions })
{
    return (
        <div>
            <div className="mb-5">
                <TransactionsFilter />
            </div>
            <Container fluid>
                <TransactionTable transactions={transactions} />
            </Container>
        </div>
    )
}

export default Transactions;
