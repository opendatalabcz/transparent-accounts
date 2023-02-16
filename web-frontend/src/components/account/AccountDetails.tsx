import { Container } from 'react-bootstrap';
import { format } from 'date-fns';
import { BsBoxArrowUpRight } from 'react-icons/bs';
import MoneyAmount from '../../features/format/MoneyAmount';
import { getAccountLink, shortenAccNum } from '../../utils/accountNumberUtils';
import { Account } from '../../types';
import './account.css';

interface Props {
  account: Account;
}

function AccountDetails({ account }: Props): JSX.Element {
  return (
    <Container fluid className="px-0">
      <dl className="account-details row mx-1">
        <dt className="col-4">Majitel účtu</dt>
        <dd className="col-8 text-end">{account.owner}</dd>

        <dt className="col-4">Název účtu</dt>
        <dd className="col-8 text-end">{account.name}</dd>

        <dt className="col-4">Číslo účtu</dt>
        <dd className="col-8 text-end">
          <a href={getAccountLink(account.number, account.bank_code)} target="_blank" rel="noreferrer">
            <BsBoxArrowUpRight className="d-inline-block align-text-top me-1" />
            {shortenAccNum(account.number)}/{account.bank_code}
          </a>
        </dd>

        <dt className="col-4">Popis</dt>
        <dd className="col-8 text-end">{account.description}</dd>

        <dt className="col-4">Datum založení</dt>
        <dd className="col-8 text-end">
          {account.created != null ? format(new Date(account.created), 'dd.MM.yyyy') : ''}
        </dd>

        <dt className="col-4">Zůstatek</dt>
        <dd className="col-8 text-end">
          <MoneyAmount amount={account.balance} currency={account.currency} />
        </dd>

        <dt className="col-4">Měna</dt>
        <dd className="col-8 text-end">{account.currency}</dd>
      </dl>
    </Container>
  );
}

export default AccountDetails;
