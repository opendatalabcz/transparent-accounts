import SearchBar from '../common/SearchBar';
import { Container } from 'react-bootstrap';
import { getAccounts } from '../../services/accountsAPI';
import { Account } from '../../types';
import { useEffect, useState } from 'react';
import AccountsTable from '../accounts/AccountsTable';
import { useNavigate } from 'react-router-dom';

const LIMIT: number = 10;

function HomePage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState<string>('');
  const [accounts, setAccounts] = useState<Array<Account>>([]);

  useEffect(() => {
    getAccounts({ limit: LIMIT }).then((accounts: Array<Account>) => setAccounts(accounts));
  }, []);

  const search = () => {
    // Remove unnecessary whitespaces
    const cleanQuery = query.trim();
    // Do not search for empty query
    if (cleanQuery === '') return;
    // Delegate search to AccountsPage
    navigate(`/ucty?query=${cleanQuery}`);
  };

  return (
    <Container>
      <SearchBar query={query} setQuery={setQuery} search={search} />
      <AccountsTable accounts={accounts} />
    </Container>
  );
}

export default HomePage;
