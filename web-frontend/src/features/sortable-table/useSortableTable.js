import { useState } from 'react';

export const useSortableTable = (data) => {
    const [tableData, setTableData] = useState(data);

    const handleSorting = (sortField, comparer, sortOrder) => {
        if (sortField) {
            const sorted = [...tableData].sort((a, b) => {
                if (a[sortField] === null) return 1;
                if (b[sortField] === null) return -1;
                if (a[sortField] === null && b[sortField] === null) return 0;
                return (
                    comparer.compare(a[sortField], b[sortField]) * (sortOrder === "asc" ? 1 : -1)
                );
            });
            setTableData(sorted);
        }
    };

    return [tableData, setTableData, handleSorting];
};