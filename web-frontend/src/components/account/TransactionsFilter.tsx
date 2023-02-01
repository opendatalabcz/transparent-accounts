import { Button, Container, Form, InputGroup } from 'react-bootstrap';
import { BsCloudDownload, BsSearch } from 'react-icons/bs';

interface Props {
  startDate: string;
  setStartDate: (startDate) => void;
  endDate: string;
  setEndDate: (endDate) => void;
  type: '' | 'INCOMING' | 'OUTGOING';
  setType: (type) => void;
  category: '' | 'CARD' | 'ATM' | 'MESSAGE' | 'NO-MESSAGE';
  setCategory: (category) => void;
  query: string;
  setQuery: (query) => void;
  downloadCSV: () => void;
}

function TransactionsFilter({
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  type,
  setType,
  category,
  setCategory,
  query,
  setQuery,
  downloadCSV
}: Props): JSX.Element {
  return (
    <Container fluid>
      <div className="row gy-2">
        <div className="col-xl-3 col-lg-6 col-12 d-flex align-items-center">
          <Form.Control
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
          />
          <span>&mdash;</span>
          <Form.Control
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
          />
        </div>
        <div className="col-xl-2 col-lg-6 col-12">
          <Form.Select value={type} onChange={(event) => setType(event.target.value)}>
            <option value="">Všechny transakce</option>
            <option value="INCOMING">Příchozí transakce</option>
            <option value="OUTGOING">Odchozí transakce</option>
          </Form.Select>
        </div>
        <div className="col-xl-2 col-lg-6 col-12">
          <Form.Select value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">Všechny kategorie</option>
            <option value="CARD">Platby kartou</option>
            <option value="ATM">Výběry z bankomatu</option>
            <option value="MESSAGE">Vzkazy</option>
            <option value="NO-MESSAGE">Bez vzkazů</option>
          </Form.Select>
        </div>
        <div className="col-xl-3 col-lg-6 col-12">
          <InputGroup>
            <InputGroup.Text>
              <BsSearch />
            </InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Hledaný výraz..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </InputGroup>
        </div>
        <div className="col-xl-2 col-12 d-flex justify-content-end">
          <Button variant="link" onClick={downloadCSV}>
            <BsCloudDownload className="d-inline-block align-text-top me-1" />
            uložit jako CSV
          </Button>
        </div>
      </div>
    </Container>
  );
}

export default TransactionsFilter;
