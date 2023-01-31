import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
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
        getTransactions(bankCode as string, accNumber as string).then(
          (transactions: Array<Transaction>) => setTransactions(transactions)
        );
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
      <Container fluid className="mt-5">
        <div className="row gy-5">
          <div className="col-xl-7 col-lg">
            <AccountMain account={account} />
          </div>
          <div className="col-xl-5 col-lg">
            <AccountDetails account={account} />
          </div>
        </div>
      </Container>
      <div className="my-3">
        <AccountSwitch setTab={setTab} />
      </div>
      <div>
        {tab === 'analyza' ? (
          <Analysis
            transactions={transactions}
            balance={account.balance}
            currency={account.currency}
          />
        ) : (
          <Transactions transactions={transactions} />
        )}
      </div>
    </main>
  );
}

export default AccountPage;
