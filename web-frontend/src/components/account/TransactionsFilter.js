import { Container, Form, InputGroup } from 'react-bootstrap';
import { BsSearch } from 'react-icons/bs'

function TransactionsFilter({ type, setType, startDate, setStartDate, endDate, setEndDate, category, setCategory, query, setQuery }) {

    return (
            <Container fluid>
                <div className="row gy-2">
                    <div className="col-xl-3 col-lg-6 d-flex align-items-center">
                        <Form.Control
                            type="date"
                            value={startDate}
                            onChange={(event) => setStartDate(event.target.value)} />
                        <span>&mdash;</span>
                        <Form.Control
                            type="date"
                            value={endDate}
                            onChange={(event) => setEndDate(event.target.value)} />
                    </div>
                    <div className="col-xl-2 col-lg-6">
                        <Form.Select
                            value={type}
                            onChange={(event) => setType(event.target.value)}>
                            <option value="ALL">Všechny transakce</option>
                            <option value="INCOMING">Příchozí transakce</option>
                            <option value="OUTGOING">Odchozí transakce</option>
                        </Form.Select>
                    </div>
                    <div className="col-xl-2 col-lg-6">
                        <Form.Select
                            value={category}
                            onChange={(event) => setCategory(event.target.value)}>
                            <option value="ALL">Všechny kategorie</option>
                            <option value="MESSAGES">Vzkazy</option>
                            <option value="NO-MESSAGES">Bez vzkazů</option>
                        </Form.Select>
                    </div>
                    <div className="col-xl-4 col-lg-6 offset-xl-1">
                        <InputGroup>
                            <InputGroup.Text><BsSearch /></InputGroup.Text>
                            <Form.Control
                                type="text"
                                placeholder="Hledaný výraz..."
                                value={query}
                                onChange={(event) => setQuery(event.target.value)} />
                        </InputGroup>
                    </div>
                </div>
            </Container>
    )
}

export default TransactionsFilter;
