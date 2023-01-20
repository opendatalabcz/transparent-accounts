function SortableTableBody({ tableData, columns }) {
    return (
        <tbody className="table-group-divider">
        {tableData.map((data) => {
            return (
                <tr key={data.id}>
                    {columns.map(({ accessor, className }) => {
                        return <td key={accessor} className={className}>{data[accessor]}</td>;
                    })}
                </tr>
            );
        })}
        </tbody>
    );
}

export default SortableTableBody;
