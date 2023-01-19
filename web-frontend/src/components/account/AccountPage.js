import { NavLink } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
import { BsChevronLeft ,BsBoxArrowUpRight } from 'react-icons/bs';

function AccountPage() {
    const account = {
        number: "000123-8794230217",
        bank_code: "0100",
        name: "Volební účet - Kampaň prezidentské volby",
        owner: "Andrej Babiš",
        balance: 222221.58,
        currency: "CZK",
        description: null,
        created: null,
        last_updated: "2023-20-01",
        last_fetched: "2023-19-01",
        archived: false,
        transactions: []
    }

    return (
        <Container fluid>
            <div className="row my-3">
                <NavLink to="/ucty">
                    <span>
                        <BsChevronLeft className="d-inline-block align-text-top me-1"/>
                        zpět na přehled
                    </span>
                </NavLink>
            </div>
            <div className="row gy-5">
                <div className="col-lg">
                    <AccountMain account={account} />
                </div>
                <div className="col-lg d-flex align-items-end">
                    <AccountDetails account={account} />
                </div>
            </div>
        </Container>

    );
}

export default AccountPage;
