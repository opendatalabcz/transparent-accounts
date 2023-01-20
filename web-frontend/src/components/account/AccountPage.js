import { NavLink } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
import { BsChevronLeft } from 'react-icons/bs';
import AccountSwitch from './AccountSwitch';
import TransactionsFilter from './TransactionsFilter';
import Transactions from './Transactions';

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

    const transactions = [
        {
            "id": 1,
            "date": "2022-01-01",
            "amount": 2345523.12,
            "counter_account": "ANO 2011",
            "type": "INCOMING",
            "type_detail": "Příchozí platba",
            "variable_symbol": "2222",
            "constant_symbol": "0",
            "specific_symbol": "0",
            "description": "Podpora"
        },
        {
            "id": 2,
            "date": "2022-01-01",
            "amount": 2345523.12,
            "counter_account": "ANO 2011",
            "type": "INCOMING",
            "type_detail": "Příchozí platba",
            "variable_symbol": "2222",
            "constant_symbol": "0",
            "specific_symbol": "0",
            "description": "Velmi dlouhá poznámka pro pana Babiše."
        },
        {
            "id": 3,
            "date": "2022-01-01",
            "amount": 2345523.12,
            "counter_account": "ANO 2011",
            "type": "INCOMING",
            "type_detail": "Příchozí platba",
            "variable_symbol": "2222",
            "constant_symbol": "0",
            "specific_symbol": "0",
            "description": "Podpora"
        }
    ]

    return (
        <main>
            <Container fluid>
                <div className="my-3 d-flex justify-content-end">
                    <NavLink to="/ucty">
                        <BsChevronLeft className="d-inline-block align-text-top me-1"/>
                        zpět na přehled
                    </NavLink>
                </div>
                <div className="row gy-5">
                    <div className="col-xl-7 col-lg">
                        <AccountMain account={account} />
                    </div>
                    <div className="col-xl-5 col-lg d-flex align-items-end">
                        <AccountDetails account={account} />
                    </div>
                </div>
            </Container>
            <div className="my-5">
                <AccountSwitch />
            </div>
            <div className="mb-5">
                <TransactionsFilter />
            </div>
            <Container fluid>
                <Transactions transactions={transactions}/>
            </Container>
        </main>
    );
}

export default AccountPage;
