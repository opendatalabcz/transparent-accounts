import { Table } from 'react-bootstrap';

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
                { transactions.map(transaction => {
                    return (
                        <tr key={transaction.id}>
                            <td>{transaction.date}</td>
                            <td className="text-end">{transaction.amount}</td>
                            <td>{transaction.type_detail}</td>
                            <td>{transaction.counter_account}</td>
                            <td>{transaction.variable_symbol}</td>
                            <td>{transaction.constant_symbol}</td>
                            <td>{transaction.specific_symbol}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.ico}</td>
                            <td>{transaction.category}</td>
                        </tr>
                    )
                }) }
                </tbody>
            </Table>
        </div>
    )
}

export default Transactions;
