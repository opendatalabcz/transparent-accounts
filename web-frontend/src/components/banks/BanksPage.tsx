import { Card, Container } from 'react-bootstrap';
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
        <Skeleton count={3} height={100} />
      ) : (
        <div className="row">
          {banks.map(
            (bank: Bank): JSX.Element => (
              <div key={bank.shortcut} className="col-12 mt-2">
                <Card className="h-100">
                  <Card.Body>
                    <Card.Title>
                      <a href={bank.url} target="_blank" rel="noreferrer">
                        {bank.name}
                      </a>
                    </Card.Title>
                    <Card.Text className="d-flex justify-content-between">
                      Počet transparentních účtů:{' '}
                      <span className="metrics-number">{bank.accounts_count}</span>
                    </Card.Text>
                  </Card.Body>
                </Card>
              </div>
            )
          )}
        </div>
      )}
    </Container>
  );
}

export default BanksPage;
