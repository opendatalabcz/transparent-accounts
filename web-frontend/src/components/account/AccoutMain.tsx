import { useEffect, useState } from 'react';
import { Button, Container, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { BsQuestionCircle } from 'react-icons/bs';
import { shortenAccNum } from '../../utils/accountNumberUtils';
import { Account } from '../../types';
import { format, isSameDay } from 'date-fns';
import { canUpdate, update } from '../../services/accountsAPI';

interface Props {
  account: Account;
}

function AccountMain({ account }: Props): JSX.Element {
  const [updatable, setUpdatable] = useState<boolean>(false);

  useEffect(() => {
    // Account was successfully update today -> not enabled
    if (account.last_fetched != null && isSameDay(new Date(account.last_fetched), new Date())) {
      setUpdatable(false);
      return;
    }
    // Check if API permits update
    canUpdate(account.bank_code, account.number).then((isPossible) => setUpdatable(isPossible));
  }, [account]);

  const sendUpdate = (): void => {
    update(account.bank_code, account.number)
      .then((location) => console.log(location))
      .catch((error) => console.log(error));
  };

  return (
    <Container fluid>
      <h1 className="display-6">
        <div>{account.owner}</div>
        <div>{account.name}</div>
        <div>
          {shortenAccNum(account.number)}/{account.bank_code}
        </div>
      </h1>
      <Button onClick={sendUpdate} disabled={!updatable}>
        Aktualizovat
      </Button>
      <div>
        Naposledy aktualizováno:{' '}
        {account.last_fetched != null ? (
          format(new Date(account.last_fetched), 'd.MM.yyyy')
        ) : (
          <span className="text-danger">nikdy</span>
        )}
        <span className="ms-1">
          <OverlayTrigger placement="bottom" overlay={<Tooltip>{/* TODO */ 'Vysvětlení'}</Tooltip>}>
            <span className="text-center">
              <BsQuestionCircle className="d-inline-block align-text-top" />
            </span>
          </OverlayTrigger>
        </span>
      </div>
    </Container>
  );
}

export default AccountMain;
