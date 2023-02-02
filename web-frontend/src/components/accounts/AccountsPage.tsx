import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import SearchBar from '../common/SearchBar';
import { Account } from '../../types';
import { getAccounts } from '../../services/accountsAPI';
import AccountsTable from './AccountsTable';

function AccountsPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState<string>(searchParams.get('query') || '');
  const [accounts, setAccounts] = useState<Array<Account>>([]);

  useEffect(() => {
    getAccounts({ query }).then((accounts: Array<Account>) => setAccounts(accounts));
  }, []);

  const search = async () => {
    // Remove unnecessary whitespaces
    const cleanQuery: string = query.trim();
    // Update URL parameters and search for accounts
    setSearchParams({ query: cleanQuery });
    getAccounts({ query: cleanQuery }).then((accounts: Array<Account>) => setAccounts(accounts));
  };

  return (
    <Container>
      <div className="row gy-5 mt-4">
        <div className="col-12">
          <SearchBar query={query} setQuery={setQuery} search={search} />
        </div>
        <div className="col-12">
          <AccountsTable accounts={accounts} />
        </div>
      </div>
    </Container>
  );
}

export default AccountsPage;
