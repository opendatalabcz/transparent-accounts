import { Container, Button } from 'react-bootstrap'
import { CiBank } from 'react-icons/ci'
import { BsQuestionCircle } from 'react-icons/bs'

function AccountMain({ account }) {
    return (
        <Container fluid className="account-main">
            <CiBank size={64}/>
            <h2>
                <div>{account.owner}</div>
                <div>{account.name}</div>
                <div>{account.number}/{account.bank_code}</div>
            </h2>
            <Button>Aktualizovat</Button>
            <div className="update-note">
                Naposledy aktualizováno: {account.last_updated}
                <BsQuestionCircle className="d-inline-block align-text-top ms-1" />
            </div>
        </Container>
    )
}

export default AccountMain;
