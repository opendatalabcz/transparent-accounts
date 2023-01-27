import { Account } from '../types';

// TODO
const URL = `http://localhost:5000`;

export const getAccount = async (bank_code: string, account_number: string): Promise<Account> => {
  const response: Response = await fetch(
    `${URL}/api/accounts/${bank_code}/${account_number}`
  );
  return await response.json();
};
