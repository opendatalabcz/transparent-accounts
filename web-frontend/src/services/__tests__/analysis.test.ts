import { getMedian } from '../analysis';
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
