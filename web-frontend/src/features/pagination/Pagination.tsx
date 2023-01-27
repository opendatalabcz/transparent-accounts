import classnames from 'classnames';
import { usePagination, DOTS } from './usePagination';
import './pagination.css';

interface Props {
  onPageChange: (number) => void;
  pageCount: number;
  siblingCount?: number;
  currentPage: number;
  className: string;
}

function Pagination({
  onPageChange,
  pageCount,
  siblingCount = 1,
  currentPage,
  className
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

  const onNext = (): void => {
    onPageChange(currentPage + 1);
  };

  const onPrevious = (): void => {
    onPageChange(currentPage - 1);
  };

  // Last page has to be number (not the dots)
  const lastPage: number = paginationRange[paginationRange.length - 1] as number;
  return (
    <ul className={classnames('pagination-container', { [className]: className })}>
      {/* Left navigation arrow */}
      <li
        className={classnames('pagination-item', {
          disabled: currentPage === 1
        })}
        onClick={onPrevious}>
        <div className="arrow left" />
      </li>
      {paginationRange.map((pageNumber) => {
        // If the pageItem is a DOT, render the DOTS unicode character
        if (pageNumber === DOTS) {
          return <li className="pagination-item dots">&#8230;</li>;
        }

        // Render our Page Pills
        return (
          <li
            className={classnames('pagination-item', {
              selected: pageNumber === currentPage
            })}
            onClick={() => onPageChange(pageNumber)}>
            {pageNumber}
          </li>
        );
      })}
      {/*  Right Navigation arrow */}
      <li
        className={classnames('pagination-item', {
          disabled: currentPage === lastPage
        })}
        onClick={onNext}>
        <div className="arrow right" />
      </li>
    </ul>
  );
}

export default Pagination;
