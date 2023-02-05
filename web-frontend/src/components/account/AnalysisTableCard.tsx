import { useMemo } from 'react';
import { Column, usePagination, useSortBy, useTable } from 'react-table';
import { Card, OverlayTrigger, Table, Tooltip } from 'react-bootstrap';
import { FaSort, FaSortDown, FaSortUp } from 'react-icons/fa';
import Pagination from '../../features/pagination/Pagination';
import { TransactionsAggregation } from '../../types';

interface AnalysisTableProps {
  tableColumns: Array<Column>;
  tableData: Array<TransactionsAggregation>;
}

function AnalysisTable({ tableColumns, tableData }: AnalysisTableProps): JSX.Element {
  const columns: Array<Column> = useMemo(() => tableColumns, [tableColumns]);
  const data: Array<any> = useMemo(() => tableData, [tableData]);

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
        pageSize: 10
      }
    },
    useSortBy,
    usePagination
  );

  return (
    <div className="table-responsive">
      <Table hover className="analysis-table" {...getTableProps()}>
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

interface AnalysisTableCardProps {
  title: string;
  columns: Array<Column>;
  data: Array<TransactionsAggregation>;
}

function AnalysisTableCard({ title, columns, data }: AnalysisTableCardProps): JSX.Element {
  return (
    <Card className="h-100">
      <Card.Body>
        <Card.Title className="h6 ellipsis mb-1">
          <OverlayTrigger placement="bottom" overlay={<Tooltip>{title}</Tooltip>}>
            <span>{title}</span>
          </OverlayTrigger>
        </Card.Title>
        <AnalysisTable tableColumns={columns} tableData={data} />
      </Card.Body>
    </Card>
  );
}

export default AnalysisTableCard;
