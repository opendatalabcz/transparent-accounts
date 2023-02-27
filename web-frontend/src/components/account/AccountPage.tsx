import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
import Transactions from './Transactions';
import Analysis from './Analysis';
import { Account, Transaction } from '../../types';
import { getAccount, getTransactions } from '../../services/accountsAPI';
import { AccountNotFound } from '../PageNotFound';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

function AccountPage(): JSX.Element {
  const { bankCode, accNumber } = useParams<Record<string, string | undefined>>();
  const [tab, setTab] = useState<'analysis' | 'transactions'>('analysis');
  const [account, setAccount] = useState<Account | null>(null);
  const [transactions, setTransactions] = useState<Array<Transaction>>([]);
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getAccount(bankCode as string, accNumber as string)
      .then((account: Account) => {
        setAccount(account);
        getTransactions(bankCode as string, accNumber as string).then(
          (transactions: Array<Transaction>) => setTransactions(transactions)
        );
      })
      .finally(() => setLoading(false));
  }, [bankCode, accNumber]);

  if (isLoading) return <Skeleton count={10} />;
  // Response from API is not 200 (Maybe distinguish between different error codes)
  if (account === null) return <AccountNotFound />;

  return (
    <main>
      <Container fluid className="mt-5 pb-1 account-info">
        <div className="row gy-5">
          <div className="col-xl-7 col-lg">
            <AccountMain account={account} tab={tab} setTab={setTab} />
          </div>
          <div className="col-xl-5 col-lg">
            <AccountDetails account={account} />
          </div>
        </div>
      </Container>
      {account.last_fetched ? (
        <div className="mt-3">
          {tab === 'transactions' ? (
            <Transactions transactions={transactions} />
          ) : (
            <Analysis account={account} transactions={transactions} />
          )}
        </div>
      ) : (
        <p className="mt-5 text-center">Prosím <span className="text-primary fw-bold text-uppercase">aktualizujte</span> účet.</p>
      )}
    </main>
  );
}

export default AccountPage;
