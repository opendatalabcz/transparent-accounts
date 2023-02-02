import SearchBar from '../common/SearchBar';
import { Container } from 'react-bootstrap';
import { getAccounts } from '../../services/accountsAPI';
import { Account } from '../../types';
import { useEffect, useState } from 'react';
import AccountsTable from './AccountsTable';
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
    // Delegate search to AccountsPage
    navigate(`/ucty?query=${cleanQuery}`);
  };

  return (
    <Container>
      <div className="row gy-5 mt-4">
        <div className="col-12">
          <SearchBar query={query} setQuery={setQuery} search={search} />
        </div>
        <div className="col-12">
          <h2 className="display-6 text-center">Naposledy aktualizované účty</h2>
          <AccountsTable accounts={accounts} />
        </div>
      </div>
    </Container>
  );
}

export default HomePage;
