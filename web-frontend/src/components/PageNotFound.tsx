import { LinkContainer } from 'react-router-bootstrap';
import { Button } from 'react-bootstrap';

function HomePage() {
    return (
        <div className="d-flex align-items-center justify-content-center vh-100">
            <div className="text-center">
                <h1 className="display-1 fw-bold">404</h1>
                <p className="fs-3"><span className="text-danger">Opps!</span> Stránka nenalezena.</p>
                <p className="lead">
                    Stránka, kterou hledáte pravděpodobně neexistuje.
                </p>
                <LinkContainer to="/">
                    <Button>
                        Zpět na úvodní stránku
                    </Button>
                </LinkContainer>
            </div>
        </div>
    );
}

export default HomePage;
