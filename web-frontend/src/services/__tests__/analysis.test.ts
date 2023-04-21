import { getMedian, analyse } from '../analysis';
import { Transaction } from '../../types';

describe('getMedian function', () => {
  test('returns null for empty array', () => {
    const transactions: Array<Transaction> = [];
    const result: number | null = getMedian(transactions);
    expect(result).toBeNull();
  });

  test('returns the median for array with odd number of elements', () => {
    const transactions: Array<Transaction> = [
      {
        id: 1,
        date: '2022-01-01',
        amount: 10,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 2,
        date: '2022-01-02',
        amount: 20,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 3,
        date: '2022-01-03',
        amount: 30,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 4,
        date: '2022-01-04',
        amount: 40,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 5,
        date: '2022-01-05',
        amount: 50,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      }
    ];
    const result: number | null = getMedian(transactions);
    expect(result).toEqual(30);
  });

  test('returns the median for array with even number of elements', () => {
    const transactions: Array<Transaction> = [
      {
        id: 1,
        date: '2022-01-01',
        amount: 10,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 2,
        date: '2022-01-02',
        amount: 20,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 1,
        date: '2022-01-01',
        amount: 30,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      },
      {
        id: 1,
        date: '2022-01-01',
        amount: 40,
        currency: 'EUR',
        type: 'INCOMING',
        type_detail: '',
        type_str: '',
        counter_account: null,
        variable_symbol: '',
        constant_symbol: '',
        specific_symbol: '',
        description: '',
        ca_identifier: null,
        ca_name: null,
        category: null
      }
    ];
    const result: number | null = getMedian(transactions);
    expect(result).toEqual(25);
  });
});

describe('analyse', () => {
  const transactions: Array<Transaction> = [
    {
      id: 3,
      date: '2022-04-21',
      amount: 100,
      currency: 'CZK',
      type: 'INCOMING',
      type_detail: 'INCOMING',
      type_str: '',
      counter_account: null,
      variable_symbol: '',
      constant_symbol: '',
      specific_symbol: '',
      description: '',
      ca_name: null,
      ca_identifier: null,
      category: null
    },
    {
      id: 2,
      date: '2022-04-20',
      amount: -50,
      currency: 'CZK',
      type: 'OUTGOING',
      type_detail: 'OUTGOING',
      type_str: '',
      counter_account: null,
      variable_symbol: '',
      constant_symbol: '',
      specific_symbol: '',
      description: 'Tisk letáků',
      ca_name: null,
      ca_identifier: null,
      category: 'Marketring'
    },
    {
      id: 1,
      date: '2022-04-19',
      amount: -75,
      currency: 'CZK',
      type: 'OUTGOING',
      type_detail: 'OUTGOING',
      type_str: '',
      counter_account: null,
      variable_symbol: '',
      constant_symbol: '',
      specific_symbol: '',
      description: 'IČO: 04434081, programátorské služby',
      ca_name: 'Profinit EU, s.r.o.',
      ca_identifier: '04434081',
      category: null
    }
  ];
  const balance = 500;
  const currency = 'CZK';

  it('returns correct analysis', () => {
    const analysis = analyse(transactions, balance, currency);
    expect(analysis.currency).toBe('CZK');
    expect(analysis.transactionsCount).toBe(3);
    expect(analysis.incomingCount).toBe(1);
    expect(analysis.outgoingCount).toBe(2);
    expect(analysis.balance).toBe(500);
    expect(analysis.incomingAmount).toBe(100);
    expect(analysis.outgoingAmount).toBe(-125);
    expect(analysis.incomingAverage).toBe(100);
    expect(analysis.outgoingAverage).toBe(-62.5);
    expect(analysis.incomingMedian).toBe(100);
    expect(analysis.outgoingMedian).toBe(-62.5);
    expect(analysis.transparency).toBe(0.5);
    expect(analysis.withDescription).toBe(1);
    expect(analysis.identifiers).toEqual([
      {
        name: 'Profinit EU, s.r.o.',
        identifier: '04434081',
        transactionsCount: 1,
        totalAmount: -75,
        currency: 'CZK'
      }
    ]);
    expect(analysis.counterAccounts).toEqual([]);
    expect(analysis.dateAggregation).toEqual([
      {
        date: '2022-04-19',
        balance: 525,
        incomingCount: 0,
        outgoingCount: 1
      },
      {
        date: '2022-04-20',
        balance: 450,
        incomingCount: 0,
        outgoingCount: 1
      },
      {
        date: '2022-04-21',
        balance: 400,
        incomingCount: 1,
        outgoingCount: 0
      },
      {
        date: '2023-04-21',
        balance: 500,
        incomingCount: 0,
        outgoingCount: 0
      }
    ]);
  });
});
