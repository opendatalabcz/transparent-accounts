import { Account } from '../../types';
import { Table } from 'react-bootstrap';
import '../common/AccountsTable.css';
import { useMemo } from 'react';
import { accountsColumns } from '../accounts/AccountsTable';
import { Column, useTable } from 'react-table';

interface Props {
  accounts: Array<Account>;
}

function AccountsTable({ accounts }: Props): JSX.Element {
  const columns: Array<Column> = useMemo(() => accountsColumns, []);
  const data: Array<Account> = useMemo(() => accounts, [accounts]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow
  } = useTable(
    {
      columns,
      data
    }
  );

  return (
    <div className="table-responsive">
      <Table hover className="accounts-table" {...getTableProps()}>
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
                  <th {...column.getHeaderProps()}>
                    {
                      // Render the header
                      column.render('Header')
                    }
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
          rows.map((row) => {
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
    </div>
  );
}

export default AccountsTable;
