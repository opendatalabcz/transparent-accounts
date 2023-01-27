import { useMemo } from 'react';

export const DOTS: string = '...';

const range = (start: number, end: number): Array<number> => {
  const length: number = end - start + 1;
  /*
  	Create an array of certain length and set the elements within it from
    start value to end value.
  */
  return Array.from({ length }, (_, idx: number): number => idx + start);
};

interface Props {
  pageCount: number;
  siblingCount: number;
  currentPage: number;
}

export const usePagination = ({
  pageCount,
  siblingCount = 1,
  currentPage
}: Props): Array<string | number> => {
  return useMemo(() => {
    // Pages count is determined as siblingCount + firstPage + lastPage + currentPage + 2*DOTS
    const totalPageNumbers: number = siblingCount + 5;

    /*
      Case 1:
      If the number of pages is less than the page numbers we want to show in our
      paginationComponent, we return the range [1..pageCount]
    */
    if (totalPageNumbers >= pageCount) {
      return range(1, pageCount);
    }

    /*
    	Calculate left and right sibling index and make sure they are within range 1 and pageCount
    */
    const leftSiblingIndex: number = Math.max(currentPage - siblingCount, 1);
    const rightSiblingIndex: number = Math.min(currentPage + siblingCount, pageCount);

    /*
      We do not show dots just when there is just one page number to be inserted between the extremes of sibling and the page limits i.e 1 and pageCount. Hence we are using leftSiblingIndex > 2 and rightSiblingIndex < pageCount - 2
    */
    const shouldShowLeftDots: boolean = leftSiblingIndex > 2;
    const shouldShowRightDots: boolean = rightSiblingIndex < pageCount - 2;

    const firstPageIndex: number = 1;
    const lastPageIndex: number = pageCount;

    /*
    	Case 2: No left dots to show, but rights dots to be shown
    */
    if (!shouldShowLeftDots && shouldShowRightDots) {
      const leftItemCount: number = 3 + 2 * siblingCount;
      const leftRange: Array<number> = range(1, leftItemCount);

      return [...leftRange, DOTS, pageCount];
    }

    /*
    	Case 3: No right dots to show, but left dots to be shown
    */
    if (shouldShowLeftDots && !shouldShowRightDots) {
      const rightItemCount: number = 3 + 2 * siblingCount;
      const rightRange: Array<number> = range(pageCount - rightItemCount + 1, pageCount);
      return [firstPageIndex, DOTS, ...rightRange];
    }

    /*
    	Case 4: Both left and right dots to be shown
    */
    if (shouldShowLeftDots && shouldShowRightDots) {
      const middleRange: Array<number> = range(leftSiblingIndex, rightSiblingIndex);
      return [firstPageIndex, DOTS, ...middleRange, DOTS, lastPageIndex];
    }

    /*
      Default: Should not happen
     */
    return [];
  }, [pageCount, siblingCount, currentPage]);
};
