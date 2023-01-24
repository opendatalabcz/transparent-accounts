import { Link } from 'react-router-dom';
import { BsBarChartFill, BsCurrencyExchange, BsBank2, BsGithub, BsChatRightTextFill, BsCodeSquare } from 'react-icons/bs';
import { Navbar, Nav } from 'react-bootstrap';
import './Header.css'

function Header() {
    return (
        <Navbar collapseOnSelect expand="lg" bg="primary" variant="dark" className="py-0 px-3">
            <Navbar.Brand>
                <Nav.Link as={Link} to="/" className="py-0 me-5" id="brand-container">
                    <div className="d-flex align-items-end">
                        <BsBarChartFill size={56} id="brand-logo" />
                        <span>
                        ZPRACOVÁNÍ A ANALÝZA{'\n'}TRANSPARENTNÍCH ÚČTŮ
                    </span>
                    </div>
                </Nav.Link>
            </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/ucty" className="me-xl-5">
                                <BsCurrencyExchange className="d-inline-block align-text-top" />
                                ÚČTY
                        </Nav.Link>
                        <Nav.Link as={Link} to="/banky" className="me-xl-5">
                            <BsBank2 className="d-inline-block align-text-top" />
                            BANKY
                        </Nav.Link>
                        <Nav.Link as={Link} to="/o-projektu" className="me-xl-5">
                            <BsChatRightTextFill className="d-inline-block align-text-top" />
                            O&nbsp;PROJEKTU
                        </Nav.Link>
                        <Nav.Link as={Link} to="/api">
                            <BsCodeSquare className="d-inline-block align-text-top" />
                            API
                        </Nav.Link>
                    </Nav>
                    <Nav>
                        <Nav.Link href="https://github.com/opendatalabcz/transparent-accounts/"
                                  target="_blank"
                                  rel="noreferrer">
                            <BsGithub className="d-inline-block align-text-top" />
                            GitHub
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
        </Navbar>
    );
}

export default Header;
