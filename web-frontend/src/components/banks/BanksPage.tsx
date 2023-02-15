import { Card, Container } from 'react-bootstrap';
import { Bank } from '../../types';
import { useEffect, useState } from 'react';
import { getBanks } from '../../services/banksAPI';

function BanksPage(): JSX.Element {
  const [banks, setBanks] = useState<Array<Bank>>([]);

  useEffect(() => {
    getBanks().then((banks: Array<Bank>) => setBanks(banks));
  }, []);

  return (
    <Container>
      <div className="d-flex justify-content-center my-4">
        <h1 className="display-6">Podporované banky 🏦</h1>
      </div>
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
    </Container>
  );
}

export default BanksPage;
