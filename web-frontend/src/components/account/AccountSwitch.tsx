import { Button, Nav } from 'react-bootstrap';

function AccountSwitch({ setTab }) {
    return (
        <Nav className="d-flex justify-content-center">
            <Nav.Item>
                <Button onClick={() => setTab('transakce')}>Transakce 💸</Button>
            </Nav.Item>
            <Nav.Item>
                <Button onClick={() => setTab('analyza')}>Analýza 📈</Button>
            </Nav.Item>
        </Nav>
    )
}

export default AccountSwitch;
