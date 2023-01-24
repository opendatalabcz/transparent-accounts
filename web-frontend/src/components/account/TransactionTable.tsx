import { useEffect, useMemo} from 'react';
import { useTable, useSortBy, useFilters, useGlobalFilter } from 'react-table'
import { Table } from 'react-bootstrap';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa'
import MoneyAmount from '../../features/format/MoneyAmount';

function TransactionTable({ transactions, date, type, category, query }) {

    const data = useMemo(() => transactions, [transactions])

    const columns = useMemo(() => [
        {
            Header: 'Datum',
            accessor: 'date',
            Cell: ({ value }) => <span className="text-nowrap">{value}</span>,
            filter: 'between'
        },
        {
            Header: 'Částka',
            accessor: 'amount',
            Cell: ({ value }) => <MoneyAmount amount={value} currency='CZK' />,
            sortDescFirst: true,
            sortType: 'basic',
        },
        {
            id: 'type',
            accessor: 'type',
        },
        {
            Header: 'Typ',
            accessor: 'type_detail',
        },
        {
            Header: 'Název protiúčtu',
            accessor: 'counter_account' },
        {
            Header: 'VS',
            accessor: 'variable_symbol' },
        {
            Header: 'KS',
            accessor: 'constant_symbol' },
        {
            Header: 'SS',
            accessor: 'specific_symbol' },
        {
            Header: 'Poznámka',
            accessor: 'description' },
        {
            Header: 'IČO',
            accessor: 'ico' },
        {
            Header: 'Kategorie',
            accessor: 'category',
            filter: 'category'
        }
    ], []);

    const filterTypes = useMemo(
        () => ({
            between: (rows, id, filterValue) => {
                return rows.filter(row => filterValue[0] <= row.values[id] && row.values[id] <= filterValue[1])
            },
            category: (rows, id, filterValue) => {
                return rows.filter(row => {
                    const rowValue = row.values[id];
                    return rowValue !== undefined
                        ? (filterValue === ''
                            || (filterValue === 'MESSAGES' && rowValue === 'Vzkaz')
                            || (filterValue === 'NO-MESSAGES' && rowValue === ''))
                        : true;
                });
            }
        }), []);

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        setFilter,
        setGlobalFilter
    } = useTable(
        {
            columns,
            data,
            filterTypes,
            initialState: {
                hiddenColumns: ['type']
            }
        },
        useFilters,
        useGlobalFilter,
        useSortBy
    )

    useEffect(() => {
        setFilter("date", date);
        setFilter("type", type);
        setFilter("category", category);
        setGlobalFilter(query)
    }, [date, type, category, query]);

    return (
        <div className='table-responsive-lg'>
            <Table striped hover className='transactions-table table-light' {...getTableProps()}>
                <thead>
                {// Loop over the header rows
                    headerGroups.map(headerGroup => (
                        // Apply the header row props
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {// Loop over the headers in each row
                                headerGroup.headers.map(column => (
                                    // Apply the header cell props
                                    <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                                        {// Render the header
                                            column.render('Header')}
                                        <span>
                                            {column.isSorted
                                                ? column.isSortedDesc
                                                    ? <FaSortDown className='d-inline-block align-text-top ms-1' />
                                                    : <FaSortUp className='d-inline-block align-text-top ms-1' />
                                                : <FaSort className='d-inline-block align-text-top ms-1' />}
                                        </span>
                                        <div>{column.id === 'type' ? column.render('Filter') : null}</div>
                                    </th>
                                ))}
                        </tr>
                    ))}
                </thead>
                {/* Apply the table body props */}
                <tbody className='table-group-divider' {...getTableBodyProps()}>
                {// Loop over the table rows
                    rows.map(row => {
                        // Prepare the row for display
                        prepareRow(row)
                        return (
                            // Apply the row props
                            <tr {...row.getRowProps()}>
                                {// Loop over the rows cells
                                    row.cells.map(cell => {
                                        // Apply the cell props
                                        return (
                                            <td {...cell.getCellProps()}>
                                                {// Render the cell contents
                                                    cell.render('Cell')}
                                            </td>
                                        )
                                    })}
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}

export default TransactionTable;
