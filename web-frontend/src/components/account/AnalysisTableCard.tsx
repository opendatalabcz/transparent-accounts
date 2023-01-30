import { useMemo } from 'react';
import { Column, usePagination, useSortBy, useTable } from 'react-table';
import { Button, Card, OverlayTrigger, Popover, Table, Tooltip } from 'react-bootstrap';
import { FaSort, FaSortDown, FaSortUp } from 'react-icons/fa';
import Pagination from '../../features/pagination/Pagination';
import { shortenAccNum } from '../../utils/accountNumberUtils';
import { Appearance, AccountShort } from '../../types';
import { BsQuestionCircle } from 'react-icons/bs';

interface renderAppearancesProps {
  value: Array<AccountShort>;
}

export const renderAppearances = ({ value }: renderAppearancesProps): JSX.Element => {
  return (
    <>
      {value.length > 0 ? (
        <OverlayTrigger
          trigger="click"
          rootClose
          placement="right"
          overlay={
            <Popover>
              <Popover.Header as="h3">
                <span>
                  Výskyty u jiných transparentních účtů
                  <OverlayTrigger
                    placement="bottom"
                    overlay={<Tooltip>{/* TODO */ 'Vysvětlení'}</Tooltip>}>
                    <span>
                      {' '}
                      <BsQuestionCircle className="d-inline-block" />
                    </span>
                  </OverlayTrigger>
                </span>
              </Popover.Header>
              <Popover.Body>
                <Table>
                  <thead>
                    <tr>
                      <th>Název účtu</th>
                      <th>Číslo účtu</th>
                    </tr>
                  </thead>
                  <tbody>
                    {value.map((account) => (
                      <tr key={account.bank_code + account.number}>
                        <td>{account.name}</td>
                        <td>
                          <a
                            target="_blank"
                            rel="noreferrer"
                            href={`/ucty/${account.bank_code}/${account.number}`}>
                            {shortenAccNum(account.number) + '/' + account.bank_code}
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Popover.Body>
            </Popover>
          }>
          <Button variant="link" className="p-0">
            {value.length}
          </Button>
        </OverlayTrigger>
      ) : (
        <span className="px-0">0</span>
      )}
    </>
  );
};

interface AnalysisTableProps {
  tableColumns: Array<Column>;
  tableData: Array<Appearance>;
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
  data: Array<Appearance>;
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
