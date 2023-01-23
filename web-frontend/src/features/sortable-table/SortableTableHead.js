import { useState } from 'react';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa'
import './table.css'

function SortableTableHead({ columns, handleSorting }) {
    const [sortField, setSortField] = useState("");
    const [order, setOrder] = useState("asc");

    const handleSortingChange = (accessor, comparer) => {
        const sortOrder =
            accessor === sortField && order === "asc" ? "desc" : "asc";
        setSortField(accessor);
        setOrder(sortOrder);
        handleSorting(accessor, comparer, sortOrder);
    };

    return (
        <thead>
            <tr>
                {columns.map(({ label, accessor, comparer, className }) => {
                    return (
                        <th
                            key={accessor}
                            className={"sortable-th " + className}
                            onClick={() => handleSortingChange(accessor, comparer)}>
                            <div>
                                {label}
                                {
                                    sortField === accessor && order === "asc"
                                        ? <FaSortUp className="d-inline-block align-text-top ms-1" />
                                        : sortField === accessor && order === "desc"
                                            ? <FaSortDown className="d-inline-block align-text-top ms-1" />
                                            : <FaSort className="d-inline-block align-text-top ms-1" />
                                }
                            </div>
                        </th>
                );
                })}
            </tr>
        </thead>
    );
}

export default SortableTableHead;
