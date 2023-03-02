import { useEffect, useState } from 'react';
import { Button, Container, OverlayTrigger, Spinner, Tooltip } from 'react-bootstrap';
import { BsInfoCircle, BsQuestionCircle } from 'react-icons/bs';
import { BiErrorCircle } from 'react-icons/bi';
import { shortenAccNum } from '../../utils/accountNumberUtils';
import { Account } from '../../types';
import { format } from 'date-fns';
import { getUpdateStatus, update } from '../../services/accountsAPI';

interface Props {
  account: Account;
  tab: 'transactions' | 'analysis';
  setTab: (tab: 'transactions' | 'analysis') => void;
}

function AccountMain({ account, tab, setTab }: Props): JSX.Element {
  const [updatable, setUpdatable] = useState<boolean>(false);
  const [isUpdating, setIsUpdating] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);

  useEffect(() => {
    getUpdateStatus(account.bank_code, account.number)
      .then((status) => {
        setUpdatable(status.updatable);
        setIsUpdating(status.status === 'PENDING');
        setIsError(status.status === 'FAILURE');
      })
      .catch(() => {
        setIsError(true);
      });
  }, [account]);

  const sendUpdate = (): void => {
    setUpdatable(false);
    setIsUpdating(true);
    setIsError(false);
    update(account.bank_code, account.number);
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
      <div className="d-flex">
        <div>
          <Button
            className="tab-button-full"
            onClick={() => setTab('analysis')}
            active={tab === 'analysis'}>
            Analyzovat 📈
          </Button>
          <Button
            className="tab-button-short"
            onClick={() => setTab('analysis')}
            active={tab === 'analysis'}>
            📈
          </Button>
        </div>
        <div className="ms-2">
          <Button
            className=" tab-button-full"
            onClick={() => setTab('transactions')}
            active={tab === 'transactions'}>
            Výpis 💸
          </Button>
          <Button
            className="tab-button-short"
            onClick={() => setTab('transactions')}
            active={tab === 'transactions'}>
            💸
          </Button>
        </div>
        <div className="separator ms-2">
          <Button onClick={sendUpdate} disabled={!updatable}>
            Aktualizovat
            {isUpdating && (
              <Spinner as="span" animation="border" size="sm" role="status" className="ms-1" />
            )}
          </Button>
        </div>
        {isUpdating && (
          <div className="ms-2">
            <OverlayTrigger
              placement="bottom"
              overlay={
                <Tooltip>Právě probíha aktualizace účtu. To může trvat jednotky sekund až minut. Zkuste prosím obnovit stránku.</Tooltip>
              }>
              <span className="update-icon">
                <BsInfoCircle />
              </span>
            </OverlayTrigger>
          </div>
        )}
        {isError && (
          <div className="ms-2 text-danger">
            <OverlayTrigger
              placement="bottom"
              overlay={
                <Tooltip>Při aktualizaci došlo k chybě. Zkuste to prosím znovu později.</Tooltip>
              }>
              <span className="update-icon">
                <BiErrorCircle />
              </span>
            </OverlayTrigger>
          </div>
        )}
      </div>
      <div className="fst-italic">
        Naposledy aktualizováno:{' '}
        {account.last_fetched != null ? (
          format(new Date(account.last_fetched), 'dd.MM.yyyy')
        ) : (
          <span className="text-danger">nikdy</span>
        )}
        <span className="ms-1">
          <OverlayTrigger
            placement="bottom"
            overlay={
              <Tooltip>
                Účet je možné aktualizovat nejvýše jednou denně a vždy jsou analyzovány všechny
                transakce do předchozího dne.
              </Tooltip>
            }>
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
