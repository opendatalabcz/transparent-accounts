import { LinkContainer } from 'react-router-bootstrap';
import { BsBarChartFill, BsCurrencyExchange, BsBank2, BsGithub, BsChatRightTextFill, BsCodeSquare } from 'react-icons/bs';
import {Navbar, Nav, Container } from "react-bootstrap";
import "./Header.css"

function Header() {
    return (
        <Navbar collapseOnSelect expand="lg" bg="primary" variant="dark" className="py-0">
                <LinkContainer to="/">
                    <Navbar.Brand>
                        <Container>
                            <div className="row">
                                <BsBarChartFill size={64} className="col pe-0"/>
                                <div className="col">
                                    ZPRACOVÁNÍ A ANALÝZA<br />TRANSPARENTNÍCH ÚČTŮ
                                </div>
                            </div>
                        </Container>
                    </Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle className="mx-2" aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav" className="ps-2">
                    <Nav className="me-auto">
                        <LinkContainer to="/ucty">
                            <Nav.Link>
                                <BsCurrencyExchange className="d-inline-block align-text-top" />{' '}
                                ÚČTY
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/banky">
                            <Nav.Link>
                                <BsBank2 className="d-inline-block align-text-top" />{' '}
                                BANKY
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/o-projektu">
                            <Nav.Link>
                                <BsChatRightTextFill className="d-inline-block align-text-top" />{' '}
                                O&nbsp;PROJEKTU
                            </Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/api">
                            <Nav.Link>
                                <BsCodeSquare className="d-inline-block align-text-top" />{' '}
                                API
                            </Nav.Link>
                        </LinkContainer>
                    </Nav>
                    <Nav>
                        <Nav.Link className="active"
                                  href="https://github.com/opendatalabcz/transparent-accounts/"
                                  target="_blank"
                                  rel="noreferrer">
                            <BsGithub className="d-inline-block align-text-top" />{' '}
                            GitHub
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
        </Navbar>
    );
}

export default Header;
