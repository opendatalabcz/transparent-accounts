import Config from '../config';
import { Bank } from '../types';

const URL = Config.API_URL;

export const getBanks = async (): Promise<Array<Bank>> => {
  const response: Response = await fetch(`${URL}/banks`);
  return await response.json();
};
