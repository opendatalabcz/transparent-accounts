import { useMemo } from 'react';
import { Column, usePagination, useSortBy, useTable } from 'react-table';
import { Table } from 'react-bootstrap';
import { FaSort, FaSortDown, FaSortUp } from 'react-icons/fa';
import Pagination from '../../features/pagination/Pagination';
import { Account } from '../../types';
import MoneyAmount from '../../features/format/MoneyAmount';
import { formatAccNum } from '../../utils/accountNumberUtils';
import { format } from 'date-fns';
import { useAccountNavigate } from '../../hooks/useAccountNavigate';

const tableColumns: Array<Column> = [
  {
    Header: 'Majitel účtu',
    accessor: 'owner'
  },
  {
    Header: 'Název účtu',
    accessor: 'name'
  },
  {
    Header: 'Číslo účtu',
    accessor: 'number',
    Cell: ({ row }) => formatAccNum(row.original.number, row.original.bank_code)
  },
  {
    accessor: 'bank_code'
  },
  {
    Header: 'Zůstatek',
    accessor: 'balance',
    Cell: ({ row }) => (
      <MoneyAmount amount={row.original.balance} currency={row.original.currency} />
    )
  },
  {
    Header: 'Aktualizováno',
    accessor: 'last_fetched',
    Cell: ({ value }) => (value != null ? format(new Date(value), 'dd.MM.yyyy') : '')
  }
];

interface Props {
  accounts: Array<Account>;
}

function AccountsTable({ accounts }: Props): JSX.Element {
  const accountNavigate = useAccountNavigate();
  const columns: Array<Column> = useMemo(() => tableColumns, [tableColumns]);
  const data: Array<Account> = useMemo(() => accounts, [accounts]);

  // Initialize the table
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    pageCount,
    gotoPage,
    state: { pageIndex }
  } = useTable(
    {
      columns,
      data,
      initialState: {
        hiddenColumns: ['bank_code'],
        pageSize: 20
      }
    },
    useSortBy,
    usePagination
  );

  return (
    <div className="table-responsive">
      <Table hover className="accounts-table table-sm" {...getTableProps()}>
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
                <tr
                  {...row.getRowProps()}
                  onClick={() => accountNavigate(row.original.number, row.original.bank_code)}>
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

export default AccountsTable;