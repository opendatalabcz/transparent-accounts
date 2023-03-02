import { useEffect, useState } from 'react';
import { Account } from '../../types';
import { getOccurrencesByCounterAccount, getOccurrencesByIdentifier } from '../../services/accountsAPI';
import { Button, OverlayTrigger, Popover, Table } from 'react-bootstrap';
import { shortenAccNum } from '../../utils/accountNumberUtils';

interface OccurrencesProps {
  occurrences: Array<Account>;
}

function Occurrences({ occurrences }: OccurrencesProps): JSX.Element {
  return (
    <>
      {occurrences.length > 0 ? (
        <OverlayTrigger
          trigger="click"
          rootClose
          placement="left"
          overlay={
            <Popover>
              <Popover.Header as="h3">
                <span>Výskyty u jiných transparentních účtů</span>
              </Popover.Header>
              <Popover.Body>
                <Table>
                  <thead>
                    <tr>
                      <th>Název účtu</th>
                      <th>Číslo účtu</th>
                    </tr>
                  </thead>
                  <tbody>
                    {occurrences.map((account) => (
                      <tr key={account.bank_code + account.number}>
                        <td>{account.name}</td>
                        <td>
                          <a
                            target="_blank"
                            rel="noreferrer"
                            href={`/ucty/${account.bank_code}/${account.number}`}>
                            {shortenAccNum(account.number) + '/' + account.bank_code}
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Popover.Body>
            </Popover>
          }>
          <Button variant="link" className="p-0">
            {occurrences.length}
          </Button>
        </OverlayTrigger>
      ) : (
        <span className="px-0">0</span>
      )}
    </>
  );
}

interface IdentifierOccurrencesProps {
  account: Account;
  identifier: string;
}

export function IdentifierOccurrences({
  account,
  identifier
}: IdentifierOccurrencesProps): JSX.Element {
  const [occurrences, setOccurrences] = useState<Array<Account>>([]);

  useEffect(() => {
    getOccurrencesByIdentifier(identifier).then((occurrences: Array<Account>) => {
      occurrences = occurrences.filter(
        (acc: Account) => acc.number !== account.number || acc.bank_code !== account.bank_code
      );
      setOccurrences(occurrences);
    });
  }, [identifier]);

  return <Occurrences occurrences={occurrences} />;
}

interface CounterAccountOccurrencesProps {
  account: Account;
  counterAccount: string;
}

export function CounterAccountOccurrences({
  account,
  counterAccount
}: CounterAccountOccurrencesProps): JSX.Element {
  const [occurrences, setOccurrences] = useState<Array<Account>>([]);

  useEffect(() => {
    getOccurrencesByCounterAccount(counterAccount).then((occurrences: Array<Account>) => {
      occurrences = occurrences.filter(
        (acc: Account) => acc.number !== account.number || acc.bank_code !== account.bank_code
      );
      setOccurrences(occurrences);
    });
  }, [counterAccount]);

  return <Occurrences occurrences={occurrences} />;
}
