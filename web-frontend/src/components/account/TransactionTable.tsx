import React from 'react';
import { useTable, useSortBy, useFilters, useGlobalFilter, useBlockLayout } from 'react-table';
import { FixedSizeList } from 'react-window';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
import MoneyAmount from '../../features/format/MoneyAmount';

function TransactionTable({ transactions, date, type, category, query }) {
  const data = React.useMemo(() => transactions, [transactions]);

  const columns = React.useMemo(
    () => [
      {
        Header: 'Datum',
        accessor: 'date',
        // Cell: ({ value }) => <span className="text-nowrap">{value}</span>,
        filter: 'between'
      },
      {
        Header: 'Částka',
        accessor: 'amount',
        Cell: ({ value }) => <MoneyAmount amount={value} currency="CZK" />,
        sortDescFirst: true,
        sortType: 'basic'
      },
      {
        id: 'type',
        accessor: 'type'
      },
      {
        Header: 'Typ',
        accessor: 'type_detail'
      },
      {
        Header: 'Název protiúčtu',
        accessor: 'counter_account'
      },
      {
        Header: 'VS',
        accessor: 'variable_symbol'
      },
      {
        Header: 'KS',
        accessor: 'constant_symbol'
      },
      {
        Header: 'SS',
        accessor: 'specific_symbol'
      },
      {
        Header: 'Poznámka',
        accessor: 'description'
      },
      {
        Header: 'IČO',
        accessor: 'ico'
      },
      {
        Header: 'Kategorie',
        accessor: 'category',
        filter: 'category'
      }
    ],
    []
  );

  const filterTypes = React.useMemo(
    () => ({
      between: (rows, id, filterValue) => {
        return rows.filter(
          (row) => filterValue[0] <= row.values[id] && row.values[id] <= filterValue[1]
        );
      },
      category: (rows, id, filterValue) => {
        return rows.filter((row) => {
          const rowValue = row.values[id];
          return rowValue !== undefined
            ? filterValue === '' ||
                (filterValue === 'MESSAGES' && rowValue === 'Vzkaz') ||
                (filterValue === 'NO-MESSAGES' && rowValue === '')
            : true;
        });
      }
    }),
    []
  );

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
    useSortBy,
    useBlockLayout
  );

  React.useEffect(() => {
    setFilter('date', date);
    setFilter('type', type);
    setFilter('category', category);
    setGlobalFilter(query);
  }, [date, type, category, query]);

  const RenderRow = React.useCallback(
    ({ index, style }) => {
      const row = rows[index];
      prepareRow(row);
      return (
        <div
          {...row.getRowProps({
            style
          })}
          className="tr">
          {row.cells.map((cell) => {
            return (
              <div {...cell.getCellProps()} className="td">
                {cell.render('Cell')}
              </div>
            );
          })}
        </div>
      );
    },
    [prepareRow, rows]
  );

  return (
    <div className="table-responsive-lg">
      <div {...getTableProps()} className="table table-light table-striped table-hover">
        <div>
          {
            // Loop over the header rows
            headerGroups.map((headerGroup) => (
              // Apply the header row props
              <div {...headerGroup.getHeaderGroupProps()} className="tr">
                {
                  // Loop over the headers in each row
                  headerGroup.headers.map((column) => (
                    // Apply the header cell props
                    <div {...column.getHeaderProps(column.getSortByToggleProps())} className="th">
                      {
                        // Render the header
                        column.render('Header')
                      }
                      <span>
                        {column.isSorted ? (
                          column.isSortedDesc ? (
                            <FaSortDown className="d-inline-block align-text-top ms-1" />
                          ) : (
                            <FaSortUp className="d-inline-block align-text-top ms-1" />
                          )
                        ) : (
                          <FaSort className="d-inline-block align-text-top ms-1" />
                        )}
                      </span>
                      <div>{column.id === 'type' ? column.render('Filter') : null}</div>
                    </div>
                  ))
                }
              </div>
            ))
          }
        </div>
        {/* Apply the table body props */}
        <div className="table-group-divider" {...getTableBodyProps()}>
          <FixedSizeList height={600} itemCount={rows.length} itemSize={40}>
            {RenderRow}
          </FixedSizeList>
        </div>
      </div>
    </div>
  );
}

export default TransactionTable;
