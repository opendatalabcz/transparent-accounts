import { useEffect, useMemo } from 'react';
import { useTable, useSortBy, useFilters, useGlobalFilter, usePagination, Column } from 'react-table';
import { Table } from 'react-bootstrap';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
import { transactionColumns } from './TransactionColumns';
import Pagination from '../../features/pagination/Pagination';
import { Transaction } from '../../types';

interface Props {
  transactions: Array<Transaction>,
  date: [string, string],
  type: string,
  category: string,
  query: string
}

function TransactionTable({ transactions, date, type, category, query }: Props): JSX.Element {
  const data: Array<Transaction> = useMemo(() => transactions, [transactions]);
  const columns: Array<Column> = useMemo(() => transactionColumns, []);

  // Definition of custom filters
  const filterTypes = useMemo(
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

  // Initialize the table
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    setFilter,
    setGlobalFilter,
    page,
    pageCount,
    gotoPage,
    state: { pageIndex }
  } = useTable(
    {
      columns,
      data,
      filterTypes,
      initialState: {
        hiddenColumns: ['type'],
        pageSize: 100
      }
    },
    useFilters,
    useGlobalFilter,
    useSortBy,
    usePagination
  );

  // Change of filters
  useEffect(() => {
    setFilter('date', date);
    setFilter('type', type);
    setFilter('category', category);
    setGlobalFilter(query);
  }, [date, type, category, query]);

  return (
    <div className="table-responsive-lg">
      <Table striped hover className="transactions-table table-light" {...getTableProps()}>
        <thead>
          {
            // Loop over the header rows
            headerGroups.map((headerGroup) => (
              // Apply the header row props
              <tr {...headerGroup.getHeaderGroupProps()}>
                {
                  // Loop over the headers in each row
                  headerGroup.headers.map((column) => (
                    // Apply the header cell props
                    <th {...column.getHeaderProps(column.getSortByToggleProps())}>
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
                    </th>
                  ))
                }
              </tr>
            ))
          }
        </thead>
        {/* Apply the pagination body props */}
        <tbody className="table-group-divider" {...getTableBodyProps()}>
          {
            // Loop over the pagination rows
            page.map((row) => {
              // Prepare the row for display
              prepareRow(row);
              return (
                // Apply the row props
                <tr {...row.getRowProps()}>
                  {
                    // Loop over the rows cells
                    row.cells.map((cell) => {
                      // Apply the cell props
                      return (
                        <td {...cell.getCellProps()}>
                          {
                            // Render the cell contents
                            cell.render('Cell')
                          }
                        </td>
                      );
                    })
                  }
                </tr>
              );
            })
          }
        </tbody>
      </Table>
      <Pagination
        className="pagination-bar"
        currentPage={pageIndex + 1}
        pageCount={pageCount}
        onPageChange={(page: number): void => gotoPage(page - 1)}
      />
    </div>
  );
}

export default TransactionTable;
