import { Container, Button, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { CiBank } from 'react-icons/ci';
import { BsQuestionCircle } from 'react-icons/bs';
import { shortenAccNum } from '../../utils/accountNumberUtils';
import { Account } from '../../types';
import dayjs from 'dayjs';
import { update } from '../../services/accounts'

interface Props {
  account: Account;
}

function AccountMain({ account }: Props): JSX.Element {

  const sendUpdate = () => {
    update(account.bank_code, account.number)
      .then(location => console.log(location))
      .catch(error => console.log(error))
  };

  return (
    <Container fluid>
      <CiBank size={64} />
      <h1 className="display-6">
        <div>{account.owner}</div>
        <div>{account.name}</div>
        <div>
          {shortenAccNum(account.number)}/{account.bank_code}
        </div>
      </h1>
      <Button onClick={sendUpdate}>Aktualizovat</Button>
      <div>
        Naposledy aktualizováno: {dayjs(account.last_updated).format('DD.MM.YYYY')}
        <span className="ms-1">
          <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip>{/* TODO */ 'Vysvětlení'}</Tooltip>}>
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
