import {Anchor, Button, Nav} from 'react-bootstrap';

function AccountSwitch() {
    return (
        <Nav className="d-flex justify-content-center">
            <Nav.Item>
                <Button>Transakce 💸</Button>
            </Nav.Item>
            <Nav.Item>
                <Button>Analýza 📈</Button>
            </Nav.Item>
        </Nav>
    )
}

export default AccountSwitch;
