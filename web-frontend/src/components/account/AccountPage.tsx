import { useEffect, useState } from 'react';
import { NavLink, useParams } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import AccountMain from './AccoutMain';
import AccountDetails from './AccountDetails';
import { BsChevronLeft } from 'react-icons/bs';
import AccountSwitch from './AccountSwitch';
import Transactions from './Transactions';
import Analysis from "./Analysis";

function AccountPage() {

    const { bankCode, accNumber } = useParams();
    const [tab, setTab] = useState('transakce')
    const [account, setAccount] = useState();
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://localhost:5000/api/accounts/0100/000000-0004070217")
            .then(response => response.json())
            .then(data => {
                setAccount(data)
                setTransactions(data.transactions)
                setLoading(false)
            }).catch(error => console.log('Error: ' + error))
    }, [])

    if (isLoading)
        return <div>Loading...</div>

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
                <AccountSwitch setTab={setTab} />
            </div>
            {tab === 'analyza' ? <Analysis /> : <Transactions transactions={transactions} />}
        </main>
    );
}

export default AccountPage;
