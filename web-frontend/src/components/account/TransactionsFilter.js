import { Container } from 'react-bootstrap';
import { BsSearch } from 'react-icons/bs'

function TransactionsFilter() {
    return (
            <Container fluid>
                <div className="row gy-2">
                    <div className="col-xl-2 col-lg-6">
                        <select className="form-select">
                            <option>06.01.2023 - 06.01.2023</option>
                        </select>
                    </div>
                    <div className="col-xl-2 col-lg-6">
                        <select className="form-select">
                            <option>Všechny transakce</option>
                            <option value="INCOMING">Příchozí transakce</option>
                            <option value="OUTGOING">Odchozí transakce</option>
                        </select>
                    </div>
                    <div className="col-xl-2 col-lg-6">
                        <select className="form-select">
                            <option>Všechny kategorie</option>
                            <option>Vzkazy</option>
                            <option>Bez vzkazů</option>
                        </select>
                    </div>
                    <div className="col-xl-4 col-lg-6 offset-xl-2">
                        <div className="input-group">
                            <span className="input-group-text"><BsSearch /></span>
                            <input type="text" className="form-control" placeholder="Hledaný výraz..."/>
                        </div>
                    </div>
                </div>
            </Container>
    )
}

export default TransactionsFilter;
