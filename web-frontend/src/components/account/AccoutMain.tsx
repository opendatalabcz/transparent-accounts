import { Container, Button } from 'react-bootstrap'
import { CiBank } from 'react-icons/ci'
import { BsQuestionCircle } from 'react-icons/bs'
import { shortenAccNum } from '../../utils/accountNumberUtils'

function AccountMain({ account }) {
    return (
        <Container fluid>
            <CiBank size={64} />
            <h1 className="display-6">
                <div>{account.owner}</div>
                <div>{account.name}</div>
                <div>{shortenAccNum(account.number)}/{account.bank_code}</div>
            </h1>
            <Button>Aktualizovat</Button>
            <div>
                Naposledy aktualizováno: {account.last_updated}
                <BsQuestionCircle className="d-inline-block align-text-top ms-1" />
            </div>
        </Container>
    )
}

export default AccountMain;
