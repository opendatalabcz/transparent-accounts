import SortableTable from '../../features/sortable-table/SortableTable';

function TransactionTable({ transactions }) {

    const columns = [
        { label: "Datum", accessor: "date", className: "" },
        { label: "Částka", accessor: "amount", className: "text-end" },
        { label: "Typ", accessor: "type_detail", className: "" },
        { label: "Název protiúčtu", accessor: "counter_account", className: "" },
        { label: "VS", accessor: "variable_symbol", className: "" },
        { label: "KS", accessor: "constant_symbol", className: "" },
        { label: "SS", accessor: "specific_symbol", className: "" },
        { label: "Poznámka", accessor: "description", className: "" },
        { label: "IČO", accessor: "ico", className: "" },
        { label: "Kategorie", accessor: "category", className: "" }
    ];

    return (
        <div className="table-responsive-lg">
            <SortableTable columns={columns} data={transactions} />
        </div>
    )
}

export default TransactionTable;
