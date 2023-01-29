import classnames from 'classnames';
import { DOTS, usePagination } from './usePagination';
import './pagination.css';

interface Props {
  onPageChange: (number) => void;
  pageCount: number;
  siblingCount?: number;
  currentPage: number;
}

function Pagination({
  onPageChange,
  pageCount,
  siblingCount = 1,
  currentPage,
}: Props): JSX.Element | null {
  const paginationRange: Array<string | number> = usePagination({
    currentPage,
    pageCount,
    siblingCount
  });

  // If there are less than 2 times in pagination range we shall not render the component
  if (currentPage === 0 || paginationRange.length < 2) {
    return null;
  }

  return (
    <ul className='pagination-container p-0'>
      {paginationRange.map((pageNumber) => {
        // If the pageItem is a DOT, render the DOTS unicode character
        if (pageNumber === DOTS) {
          return <li className="pagination-item dots">&#8230;</li>;
        }
        // Render our Page Pills
        return (
          <li
            className={classnames('pagination-item number', {
              selected: pageNumber === currentPage
            })}
            onClick={() => onPageChange(pageNumber)}>
            {pageNumber}
          </li>
        );
      })}
    </ul>
  );
}

export default Pagination;
