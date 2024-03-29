import { useEffect, useMemo } from 'react';
import {
  Column,
  useFilters,
  useGlobalFilter,
  usePagination,
  useSortBy,
  useTable
} from 'react-table';
import { Table } from 'react-bootstrap';
import { FaSort, FaSortDown, FaSortUp } from 'react-icons/fa';
import { transactionsColumns } from './TransactionsColumns';
import Pagination from '../../features/pagination/Pagination';
import { Transaction } from '../../types';

interface Props {
  transactions: Array<Transaction>;
  date: [string, string];
  type: string;
  category: string;
  query: string;
}

function TransactionTable({ transactions, date, type, category, query }: Props): JSX.Element {
  const data: Array<Transaction> = useMemo(() => transactions, [transactions]);
  const columns: Array<Column> = useMemo(() => transactionsColumns, []);

  // Definition of custom filters
  const filterTypes = useMemo(
    () => ({
      date: (rows, id, filterValue) => {
        return rows.filter(
          (row) =>
            (filterValue[0] === '' || filterValue[0] <= row.values[id]) &&
            (filterValue[1] === '' || row.values[id] <= filterValue[1])
        );
      },
      category: (rows, id, filterValue) => {
        return rows.filter((row) => {
          const rowValue = row.values[id];
          return rowValue !== undefined
            ? filterValue === '' ||
                filterValue === rowValue ||
                (filterValue === 'NO-MESSAGES' && rowValue !== 'Vzkaz')
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
      <Table hover className="transactions-table" {...getTableProps()}>
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
                    <th
                      {...column.getHeaderProps(column.getSortByToggleProps({ title: undefined }))}>
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
      <div className="d-flex justify-content-center">
        <Pagination
          currentPage={pageIndex + 1}
          pageCount={pageCount}
          onPageChange={(page: number): void => gotoPage(page - 1)}
        />
      </div>
    </div>
  );
}

export default TransactionTable;
