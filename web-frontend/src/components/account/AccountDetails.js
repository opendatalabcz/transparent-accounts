import { Container, Anchor } from 'react-bootstrap'
import { BsBoxArrowUpRight } from 'react-icons/bs'
import './account.css'

function AccountDetails({ account }) {
    return (
        <Container fluid className="px-0">
            <dl className="account-details row mx-1">
                <dt className="col-4">Majitel účtu</dt>
                <dd className="col-8 text-end">{account.owner}</dd>

                <dt className="col-4">Název účtu</dt>
                <dd className="col-8 text-end">{account.name}</dd>

                <dt className="col-4">Číslo účtu</dt>
                <dd className="col-8 text-end">{account.number}/{account.bank_code}</dd>

                <dt className="col-4">Popis</dt>
                <dd className="col-8 text-end">{account.description}</dd>

                <dt className="col-4">Datum založení</dt>
                <dd className="col-8 text-end">{account.created}</dd>

                <dt className="col-4">Zůstatek 💰</dt>
                <dd className="col-8 text-end">{account.balance} {account.currency}</dd>

                <dt className="col-4">Měna</dt>
                <dd className="col-8 text-end">{account.currency}</dd>
            </dl>
            <div className="d-flex justify-content-end">
                <Anchor href="https://www.csas.cz/cs/transparentni-ucty" target="_blank" rel="noreferrer">
                    <BsBoxArrowUpRight className="d-inline-block align-text-top me-1"/>
                    účet na stránkách banky
                </Anchor>
            </div>
        </Container>
    )
}

export default AccountDetails;
