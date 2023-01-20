function Transaction({ transaction }) {
    return (
        <tr>
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
}

export default Transaction;
