import { useEffect, useState } from 'react';
import { NavLink, useParams } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
import { BsChevronLeft } from 'react-icons/bs';
import AccountSwitch from './AccountSwitch';
import Transactions from './Transactions';
import Analysis from './Analysis';
import { Account, Transaction } from '../../types';
import { getAccount, getTransactions } from '../../services/accountsAPI';

function AccountPage() {
  const { bankCode, accNumber } = useParams<Record<string, string | undefined>>();
  const [tab, setTab] = useState<'transakce' | 'analyza'>('transakce');
  const [account, setAccount] = useState<Account | null>(null);
  const [transactions, setTransactions] = useState<Array<Transaction>>([]);
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getAccount(bankCode as string, accNumber as string)
      .then((account: Account) => {
        setAccount(account);
        getTransactions(bankCode as string, accNumber as string)
          .then((transactions: Array<Transaction>) => setTransactions(transactions))
      })
      .catch((error) => console.log('Error: ' + error))
      .finally(() => setLoading(false));
  }, [bankCode, accNumber]);

  // TODO
  if (isLoading) return <div>Loading...</div>;
  // TODO
  if (account === null) return <div>Account not found</div>;

  return (
    <main>
      <Container fluid>
        <div className="d-flex justify-content-end mt-3">
          <NavLink to="/ucty">
            <BsChevronLeft className="d-inline-block align-text-top me-1" />
            zpět na přehled
          </NavLink>
        </div>
        <div className="row gy-5">
          <div className="col-xl-7 col-lg">
            <AccountMain account={account} />
          </div>
          <div className="col-xl-5 col-lg d-flex align-items-end">
            <AccountDetails account={account} />
          </div>
        </div>
      </Container>
      <div className="my-5">
        <AccountSwitch setTab={setTab} />
      </div>
      <div>
        {tab === 'analyza' ? <Analysis /> : <Transactions transactions={transactions} />}
      </div>
    </main>
  );
}

export default AccountPage;
