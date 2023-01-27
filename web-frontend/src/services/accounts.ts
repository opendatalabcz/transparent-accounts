import { Account } from '../types';

// TODO
const URL = `http://localhost:5000`;

export const getAccount = async (bank_code: string, account_number: string): Promise<Account> => {
  const response: Response = await fetch(`${URL}/api/accounts/${bank_code}/${account_number}`);
  return await response.json();
};

export const update = async (bank_code: string, account_number: string): Promise<string | null> => {
  const response: Response = await fetch(
    `${URL}/api/accounts/${bank_code}/${account_number}/updates`,
    {
      method: 'POST'
    }
  );
  // TODO: due to CORS policy, the response does not contain the Location header
  return response.headers.get('Location');
};
