export interface Account {
  number: string;
  bank_code: string;
  name: string | null;
  owner: string;
  balance: number | null;
  currency: string | null;
  description: string | null;
  created: string | null;
  last_updated: string;
  last_fetched: string | null;
  archived: boolean;
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
  ca_identifier: string | null;
  ca_name: string | null;
  category: string | null;
}

export interface UpdateStatus {
  status: 'PENDING' | 'SUCCESS' | 'FAILED';
  updatable: boolean;
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
  withDescription: number | null;
  identifiers: Array<TransactionsAggregation>;
  counterAccounts: Array<TransactionsAggregation>;
  dateAggregation: Array<DateCounts>;
}

export interface DateCounts {
  date: string;
  balance?: number;
  incomingCount: number;
  outgoingCount: number;
}

export interface TransactionsAggregation {
  name: string;
  identifier?: string;
  transactionsCount: number;
  totalAmount: number;
  currency: string;
}

export interface Bank {
  shortcut: string;
  name: string;
  code: string;
  url: string;
  accounts_count: number;
}
