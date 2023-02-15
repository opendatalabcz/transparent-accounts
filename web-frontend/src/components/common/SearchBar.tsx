import { Button, Form, InputGroup } from 'react-bootstrap';

interface Props {
  query: string;
  setQuery: (query: string) => void;
  search: () => void;
}

function SearchBar({ query, setQuery, search }: Props): JSX.Element {
  return (
    <div className="d-flex justify-content-center">
      <div>
        <h1 className="display-6">Vyhledání transparentního účtu 💸</h1>
        <InputGroup className="row mt-4">
          <Form.Control
            type="text"
            placeholder="Hledaný výraz..."
            value={query}
            className="col-9"
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                search();
              }
            }}
          />
          <Button variant="outline-dark" className="col-3" onClick={search}>
            Vyhledat
          </Button>
        </InputGroup>
      </div>
    </div>
  );
}

export default SearchBar;
