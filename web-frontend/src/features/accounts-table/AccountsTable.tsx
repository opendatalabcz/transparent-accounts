import { Account } from '../../types';
import { Table } from 'react-bootstrap';
import { formatAccNum } from '../../utils/accountNumberUtils';
import MoneyAmount from '../format/MoneyAmount';
import { format } from 'date-fns';
import './AccountsTable.css';
import { useNavigate } from 'react-router-dom';

interface Props {
  accounts: Array<Account>;
}

function AccountsTable({ accounts }: Props): JSX.Element | null {
  const navigate = useNavigate();
  const selectAccount = (accountNumber: string, bankCode: string): void => {
    navigate(`/ucty/${bankCode}/${accountNumber}`);
  };

  // Empty source data - do not render anything
  if (accounts.length === 0) {
    return null;
  }

  return (
    <div className="table-responsive">
      <Table hover className="accounts-table">
        <thead>
          <tr>
            <th>Majitel účtu</th>
            <th>Číslo účtu</th>
            <th>Zůstatek</th>
            <th>Aktualizováno</th>
          </tr>
        </thead>
        <tbody className="table-group-divider">
          {accounts.map((account: Account) => (
            <tr
              key={formatAccNum(account.number, account.bank_code)}
              onClick={() => selectAccount(account.number, account.bank_code)}>
              <td>{account.owner}</td>
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
