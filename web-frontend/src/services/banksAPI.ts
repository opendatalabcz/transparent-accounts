import { Bank } from '../types';

// TODO
const URL = `http://localhost:5000`;

export const getBanks = async (): Promise<Array<Bank>> => {
  const response: Response = await fetch(`${URL}/api/banks`);
  return await response.json();
};
