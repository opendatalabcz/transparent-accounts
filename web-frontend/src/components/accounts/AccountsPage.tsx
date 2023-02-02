import { useState } from 'react';
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

  const search = async () => {
    // Remove unnecessary whitespaces
    const cleanQuery: string = query.trim();
    // Do not search for empty query
    if (cleanQuery === '') return;
    // Update URL parameters and search for accounts
    setSearchParams({ query: cleanQuery });
    getAccounts({ query: cleanQuery }).then((accounts: Array<Account>) => setAccounts(accounts));
  };

  return (
    <Container>
      <SearchBar query={query} setQuery={setQuery} search={search} />
      <AccountsTable accounts={accounts} />
    </Container>
  );
}

export default AccountsPage;
