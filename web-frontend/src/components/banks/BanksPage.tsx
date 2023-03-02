import { Container, Table } from 'react-bootstrap';
import { Bank } from '../../types';
import { useEffect, useState } from 'react';
import { getBanks } from '../../services/banksAPI';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

function BanksPage(): JSX.Element {
  const [banks, setBanks] = useState<Array<Bank>>([]);
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getBanks().then((banks: Array<Bank>) => {
      setBanks(banks);
      setLoading(false);
    });
  }, []);

  return (
    <Container>
      <h1 className="my-4 text-center">Podporované banky 🏦</h1>
      {isLoading ? (
        <Skeleton count={8} height={25} />
      ) : (
        <Table striped hover bordered>
          <thead>
            <tr>
              <th scope="col">Název</th>
              <th scope="col">Počet transparentních účtů</th>
            </tr>
          </thead>
          <tbody>
            {banks.map(
              (bank: Bank): JSX.Element => (
                <tr key={bank.shortcut}>
                  <td>
                    <a href={bank.url} target="_blank" rel="noreferrer">
                      {bank.name}
                    </a>
                  </td>
                  <td>{bank.accounts_count}</td>
                </tr>
              )
            )}
          </tbody>
        </Table>
      )}
    </Container>
  );
}

export default BanksPage;
