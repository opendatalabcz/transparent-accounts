import { Button, Nav } from 'react-bootstrap';

interface Props {
  setTab: (tab: 'transakce' | 'analyza') => void
}

function AccountSwitch({ setTab }: Props): JSX.Element {
  return (
    <Nav className="d-flex justify-content-center">
      <Nav.Item>
        <Button onClick={() => setTab('transakce')}>Transakce 💸</Button>
      </Nav.Item>
      <Nav.Item>
        <Button onClick={() => setTab('analyza')}>Analýza 📈</Button>
      </Nav.Item>
    </Nav>
  );
}

export default AccountSwitch;
