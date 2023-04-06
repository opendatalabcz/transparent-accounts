import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import SearchBar from '../common/SearchBar';
import { Account } from '../../types';
import { getAccounts } from '../../services/accountsAPI';
import AccountsTable from './AccountsTable';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

function AccountsPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState<string>(searchParams.get('query') || '');
  const [accounts, setAccounts] = useState<Array<Account>>([]);
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    search();
  }, []);

  const search = async () => {
    setLoading(true);
    // Remove unnecessary whitespaces
    const cleanQuery: string = query.trim();
    // Query is empty, show most recently updated accounts and remove query parameter from URL
    if (cleanQuery === '') {
      getAccounts({ limit: 20 }).then((accounts: Array<Account>) => {
        setAccounts(accounts);
        setLoading(false);
      });
      // Remove query parameter from URL
      if (searchParams.has('query')) {
        searchParams.delete('query');
        setSearchParams(searchParams);
      }
      return;
    }
    // Update URL parameters and search for accounts
    setSearchParams({ query: cleanQuery });
    getAccounts({ query: cleanQuery }).then((accounts: Array<Account>) => {
      setAccounts(accounts);
      setLoading(false);
    });
  };

  return (
    <Container>
      <div className="row my-4">
        <SearchBar query={query} setQuery={setQuery} search={search} />
      </div>
      <div className="row">
        {accounts.length === 0 && !isLoading ? (
          <></>
        ) : isLoading ? (
          <Skeleton count={20} height={25} />
        ) : (
          <AccountsTable accounts={accounts} />
        )}
      </div>
    </Container>
  );
}

export default AccountsPage;
