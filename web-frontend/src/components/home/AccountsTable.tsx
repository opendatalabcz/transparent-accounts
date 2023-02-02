import { Account } from '../../types';
import { Table } from 'react-bootstrap';
import { formatAccNum } from '../../utils/accountNumberUtils';
import MoneyAmount from '../../features/format/MoneyAmount';
import { format } from 'date-fns';
import '../common/AccountsTable.css';
import { useAccountNavigate } from '../../hooks/useAccountNavigate';

interface Props {
  accounts: Array<Account>;
}

function AccountsTable({ accounts }: Props): JSX.Element | null {
  const accountNavigate = useAccountNavigate();

  return (
    <div className="table-responsive">
      <Table hover className="accounts-table">
        <thead>
          <tr>
            <th>Majitel účtu</th>
            <th>Název účtu</th>
            <th>Číslo účtu</th>
            <th>Zůstatek</th>
            <th>Aktualizováno</th>
          </tr>
        </thead>
        <tbody className="table-group-divider">
          {accounts.map((account: Account) => (
            <tr
              key={formatAccNum(account.number, account.bank_code)}
              onClick={() => accountNavigate(account.number, account.bank_code)}>
              <td>{account.owner}</td>
              <td>{account.name}</td>
              <td>{formatAccNum(account.number, account.bank_code)}</td>
              <td>
                <MoneyAmount amount={account.balance} currency={account.currency} />
              </td>
              <td>
                {account.last_fetched != null
                  ? format(new Date(account.last_fetched), 'dd.MM.yyyy')
                  : ''}
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default AccountsTable;
