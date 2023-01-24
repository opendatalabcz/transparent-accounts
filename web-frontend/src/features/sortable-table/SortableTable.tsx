import { useEffect } from 'react';
import { Table } from 'react-bootstrap'
import { useSortableTable } from './useSortableTable';
import TableHead from './SortableTableHead';
import TableBody from './SortableTableBody';

function SortableTable({ columns, data }) {
    const [tableData, setTableData, handleSorting] = useSortableTable(data);

    useEffect(() => setTableData(data), [data])

    return (
        <Table striped hover className="transactions-table table-light">
            <TableHead {...{ columns, handleSorting }} />
            <TableBody {...{ columns, tableData }} />
        </Table>
    );
}

export default SortableTable;
