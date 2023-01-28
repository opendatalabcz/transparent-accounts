export interface Account {
  number: string,
  bank_code: string,
  name: string | null,
  owner: string,
  balance: number | null,
  currency: string | null,
  description: string | null,
  created: string | null,
  last_updated: string,
  last_fetched: string | null,
  archived: boolean
}

export interface Transaction {
  id: number;
  date: string;
  amount: number;
  currency: string;
  type: 'INCOMING' | 'OUTGOING';
  type_detail: string;
  counter_account: string | null;
  variable_symbol: string;
  constant_symbol: string;
  specific_symbol: string;
  description: string;
  identifier: string | null;
  category: string | null;
}

export interface Analysis {
  currency: string | null;
  transactionsCount: number;
  incomingCount: number;
  outgoingCount: number;
  balance: number | null;
  incomingAmount: number;
  outgoingAmount: number;
  incomingAverage: number | null;
  outgoingAverage: number | null;
  incomingMedian: number | null;
  outgoingMedian: number | null;
  transparency: number | null;
  noted: number | null;
}
