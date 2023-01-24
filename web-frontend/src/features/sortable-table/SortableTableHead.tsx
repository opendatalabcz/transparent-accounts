import { useState } from 'react';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa'
import './table.css'

function SortableTableHead({ columns, handleSorting }) {
    const [sortField, setSortField] = useState("");
    const [order, setOrder] = useState("desc");

    const handleSortingChange = (accessor, comparer) => {
        const sortOrder =
            accessor === sortField && order === "desc" ? "asc" : "desc";
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
                                    sortField === accessor && order === "desc"
                                        ? <FaSortUp className="d-inline-block align-text-top ms-1" />
                                        : sortField === accessor && order === "asc"
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
