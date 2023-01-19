import { LinkContainer } from 'react-router-bootstrap';
import { BsBarChartFill, BsCurrencyExchange, BsBank2, BsGithub, BsChatRightTextFill, BsCodeSquare } from 'react-icons/bs';
import { Navbar, Nav } from 'react-bootstrap';
import './Header.css'

function Header() {
    return (
        <Navbar collapseOnSelect expand="lg" bg="primary" variant="dark" className="py-0 px-3">
                <LinkContainer to="/" className="py-0 me-5">
                    <Navbar.Brand>
                                <BsBarChartFill size={56} />
                                <span>
                                    ZPRACOVÁNÍ A ANALÝZA{'\n'}TRANSPARENTNÍCH ÚČTŮ
                                </span>
                    </Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <LinkContainer to="/ucty" className="me-xl-5">
                            <Nav.Link active={false}>
                                <BsCurrencyExchange className="d-inline-block align-text-top" />
                                ÚČTY
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/banky" className="me-xl-5">
                            <Nav.Link active={false}>
                                <BsBank2 className="d-inline-block align-text-top" />
                                BANKY
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/o-projektu" className="me-xl-5">
                            <Nav.Link active={false}>
                                <BsChatRightTextFill className="d-inline-block align-text-top" />
                                O&nbsp;PROJEKTU
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/api">
                            <Nav.Link active={false}>
                                <BsCodeSquare className="d-inline-block align-text-top" />
                                API
                            </Nav.Link>
                        </LinkContainer>
                    </Nav>
                    <Nav>
                        <Nav.Link active={false}
                                  href="https://github.com/opendatalabcz/transparent-accounts/"
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
