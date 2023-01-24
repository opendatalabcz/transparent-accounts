import SortableTable from '../../features/sortable-table/SortableTable';
import MoneyAmount from "../../features/format/MoneyAmount";

function TransactionTable({ transactions }) {

    transactions = transactions.map(transaction => {
        return {...transaction, moneyAmount: <MoneyAmount amount={transaction.amount} currency={transaction.currency}/> }
    })

    const csComparer = new Intl.Collator("cs");
    const moneyComparer = {
        compare: (a, b) => a.props.amount - b.props.amount
    }

    const columns = [
        { label: "Datum", accessor: "date", comparer: csComparer, className: "" },
        { label: "Částka", accessor: "moneyAmount", comparer: moneyComparer, className: "text-end" },
        { label: "Typ", accessor: "type_detail", comparer: csComparer, className: "" },
        { label: "Název protiúčtu", accessor: "counter_account", comparer: csComparer, className: "" },
        { label: "VS", accessor: "variable_symbol", comparer: csComparer, className: "" },
        { label: "KS", accessor: "constant_symbol", comparer: csComparer, className: "" },
        { label: "SS", accessor: "specific_symbol", comparer: csComparer, className: "" },
        { label: "Poznámka", accessor: "description", comparer: csComparer, className: "" },
        { label: "IČO", accessor: "ico", comparer: csComparer, className: "" },
        { label: "Kategorie", accessor: "category", comparer: csComparer, className: "" }
    ];

    return (
        <div className="table-responsive-lg">
            <SortableTable columns={columns} data={transactions} />
        </div>
    )
}

export default TransactionTable;
