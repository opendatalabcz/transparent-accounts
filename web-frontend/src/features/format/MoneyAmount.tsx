interface Props {
  amount: number | null;
  currency: string | null;
}

function MoneyAmount({ amount, currency }: Props): JSX.Element | null {
  if (amount === null || currency === null) return null;

  return (
    <span
      className={
        'money-amount text-nowrap fw-bold ' + (amount != null && amount < 0 ? 'text-danger' : '')
      }>
      {amount != null ? amount.toLocaleString('cs-CZ', { minimumFractionDigits: 2 }) : ''}{' '}
      {currency}
    </span>
  );
}

export default MoneyAmount;
