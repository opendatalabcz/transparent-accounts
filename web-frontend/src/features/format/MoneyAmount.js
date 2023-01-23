function MoneyAmount({ amount, currency }) {
    return (
        <span className={"fw-bold " + (amount < 0 ? "text-danger" : "")}>
            {amount.toLocaleString('cs-CZ', {minimumFractionDigits: 2})} {currency}
        </span>
    )
}

export default MoneyAmount;
