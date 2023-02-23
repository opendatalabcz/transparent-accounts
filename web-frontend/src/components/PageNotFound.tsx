import { Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';

export function AccountNotFound(): JSX.Element {
  return (
    <div className="not-found-page d-flex align-items-center justify-content-center">
      <div className="text-center">
        <h1 className="display-1 fw-bold">404</h1>
        <p className="fs-3">
          <span className="text-danger">Ups!</span> Účet nenalezen.
        </p>
        <p className="lead">Účet, který hledáte pravděpodobně neexistuje.</p>
        <Link to="/ucty">
          <Button>Zpět na stránku s účty</Button>
        </Link>
      </div>
    </div>
  );
}

function PageNotFound(): JSX.Element {
  return (
    <div className="not-found-page d-flex align-items-center justify-content-center">
      <div className="text-center">
        <h1 className="display-1 fw-bold">404</h1>
        <p className="fs-3">
          <span className="text-danger">Ups!</span> Stránka nenalezena.
        </p>
        <p className="lead">Stránka, kterou hledáte pravděpodobně neexistuje.</p>
        <Link to="/">
          <Button>Zpět na úvodní stránku</Button>
        </Link>
      </div>
    </div>
  );
}

export default PageNotFound;
