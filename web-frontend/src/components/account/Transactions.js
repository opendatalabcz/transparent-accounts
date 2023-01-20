import { Table } from 'react-bootstrap';
import Transaction from './Transaction'

function Transactions({ transactions }) {
    return (
        <div className="table-responsive-lg">
            <Table striped hover className="transactions-table table-light">
                <thead>
                <tr>
                    <th scope="col">Datum</th>
                    <th scope="col" className="text-end">Částka</th>
                    <th scope="col">Typ</th>
                    <th scope="col">Název protiúčtu</th>
                    <th scope="col">VS</th>
                    <th scope="col">KS</th>
                    <th scope="col">SS</th>
                    <th scope="col">Poznámka</th>
                    <th scope="col">IČO</th>
                    <th scope="col">Kategorie</th>
                </tr>
                </thead>
                <tbody className="table-group-divider">
                    {
                        transactions.map(transaction => <Transaction key={transaction.id} transaction={transaction} />)
                    }
                </tbody>
            </Table>
        </div>
    )
}

export default Transactions;
