import { Account, Transaction, UpdateStatus } from '../types';

// TODO
const URL = `http://localhost:5000`;

export const getAccount = async (bank_code: string, account_number: string): Promise<Account> => {
  const response: Response = await fetch(`${URL}/api/accounts/${bank_code}/${account_number}`);
  return await response.json();
};

export const getAccounts = async ({
  query,
  limit
}: {
  query?: string;
  limit?: number;
}): Promise<Array<Account>> => {
  // Resolve query params
  let params: string = 'order_by=last_fetched';
  if (query) params += `&query=${query}`;
  if (limit) params += `&limit=${limit}`;

  const response: Response = await fetch(`${URL}/api/accounts?${params}`);
  return await response.json();
};

export const getTransactions = async (
  bank_code: string,
  account_number: string
): Promise<Array<Transaction>> => {
  const response: Response = await fetch(
    `${URL}/api/accounts/${bank_code}/${account_number}/transactions`
  );
  return await response.json();
};

export const getUpdateStatus = async (
  bank_code: string,
  account_number: string
): Promise<UpdateStatus> => {
  const response: Response = await fetch(
    `${URL}/api/accounts/${bank_code}/${account_number}/status`
  );
  return await response.json();
};

export const update = async (bank_code: string, account_number: string): Promise<void> => {
  await fetch(
    `${URL}/api/accounts/${bank_code}/${account_number}/updates`,
    {
      method: 'POST'
    }
  );
};

export const getOccurrencesByIdentifier = async (identifier: string): Promise<Array<Account>> => {
  const response: Response = await fetch(`${URL}/api/occurrences?identifier=${identifier}`);
  return await response.json();
};

export const getOccurrencesByCounterAccount = async (
  counterAccount: string
): Promise<Array<Account>> => {
  const response: Response = await fetch(
    `${URL}/api/occurrences?counter_account=${counterAccount}`
  );
  return await response.json();
};
