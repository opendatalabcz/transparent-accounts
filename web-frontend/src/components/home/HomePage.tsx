import SearchBar from '../common/SearchBar';
import { Container } from 'react-bootstrap';
import { getAccounts } from '../../services/accountsAPI';
import { Account } from '../../types';
import { useEffect, useState } from 'react';
import AccountsTable from './AccountsTable';
import { useNavigate } from 'react-router-dom';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const LIMIT: number = 10;

function HomePage(): JSX.Element {
  const navigate = useNavigate();
  const [query, setQuery] = useState<string>('');
  const [accounts, setAccounts] = useState<Array<Account>>([]);
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getAccounts({ limit: LIMIT }).then((accounts: Array<Account>) => {
      setAccounts(accounts);
      setLoading(false);
    });
  }, []);

  const search = () => {
    // Remove unnecessary whitespaces
    const cleanQuery = query.trim();
    // Delegate search to AccountsPage
    navigate(`/ucty?query=${cleanQuery}`);
  };

  return (
    <Container>
      <div className="row my-4">
        <SearchBar query={query} setQuery={setQuery} search={search} />
      </div>
      <div className="row">
        <h2 className="display-6 text-center">Naposledy aktualizované účty</h2>
        {isLoading ? <Skeleton count={15} /> : <AccountsTable accounts={accounts} />}
      </div>
    </Container>
  );
}

export default HomePage;
