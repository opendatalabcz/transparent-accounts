import { Analysis, Transaction } from '../types';
import { format } from 'date-fns';

export const analyse = (
  transactions: Array<Transaction>,
  balance: number | null,
  currency: string | null
): Analysis => {
  // Create an empty Analysis instance
  const analysis: Analysis = {} as Analysis;
  // Set known values
  analysis.balance = balance;
  analysis.currency = currency;
  analysis.transactionsCount = transactions.length;
  // Set initial values
  analysis.incomingAmount = 0;
  analysis.outgoingAmount = 0;
  analysis.dateAggregation = [];

  // Create auxiliary variables
  const incomingTransactions: Array<Transaction> = [];
  const outgoingTransactions: Array<Transaction> = [];
  let transparentNoteCount: number = 0;
  let noteCount: number = 0;
  // Calculate first set of values
  transactions.forEach((transaction: Transaction) => {
    if (transaction.type === 'INCOMING') {
      incomingTransactions.push(transaction);
      analysis.incomingAmount += transaction.amount;
    } else if (transaction.type === 'OUTGOING') {
      outgoingTransactions.push(transaction);
      analysis.outgoingAmount += transaction.amount;
      transparentNoteCount =
        transaction.identifier !== null ? transparentNoteCount + 1 : transparentNoteCount;
      noteCount = transaction.description !== '' ? noteCount + 1 : noteCount;
    }
  });
  // Set calculated values
  analysis.incomingCount = incomingTransactions.length;
  analysis.outgoingCount = outgoingTransactions.length;
  analysis.incomingAverage = analysis.incomingAmount / analysis.incomingCount;
  analysis.outgoingAverage = analysis.outgoingAmount / analysis.outgoingCount;
  analysis.incomingMedian = getMedian(incomingTransactions);
  analysis.outgoingMedian = getMedian(outgoingTransactions);
  analysis.transparency = transparentNoteCount / analysis.outgoingCount;
  analysis.noted = noteCount / analysis.outgoingCount;

  // Create auxiliary variables
  let currentBalance: number = balance || 0;
  let lastDate: string = format(new Date(), 'yyyy-MM-d');
  analysis.dateAggregation.push({
    date: lastDate,
    balance: currentBalance,
    incomingCount: 0,
    outgoingCount: 0
  });
  // Calculate second set of values
  transactions.forEach((transaction: Transaction) => {
    if (lastDate !== transaction.date) {
      lastDate = transaction.date;
      analysis.dateAggregation.push({
        date: lastDate,
        balance: 0,
        incomingCount: 0,
        outgoingCount: 0
      });
    }
    currentBalance -= transaction.amount;
    analysis.dateAggregation[analysis.dateAggregation.length - 1].balance = currentBalance;
    analysis.dateAggregation[analysis.dateAggregation.length - 1].incomingCount +=
      transaction.type === 'INCOMING' ? 1 : 0;
    analysis.dateAggregation[analysis.dateAggregation.length - 1].outgoingCount +=
      transaction.type === 'OUTGOING' ? 1 : 0;
  });
  // Reverse the array
  analysis.dateAggregation.reverse();

  // TODO remove example data and add implementation
  analysis.identifiers = [
    {
      name: '04434081',
      appearances: [
        { number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' },
        { number: '000000-2902252345', bank_code: '2010', name: 'generalpavel' },
        { number: '000000-0004070217', bank_code: '0100', name: 'ANO 2011' }
      ],
      transactionsCount: 7,
      totalAmount: -3265434
    },
    {
      name: '12345678',
      appearances: [],
      transactionsCount: 1,
      totalAmount: -25000
    },
    {
      name: '12345678',
      appearances: [],
      transactionsCount: 1,
      totalAmount: -25000
    },
    {
      name: '12345678',
      appearances: [],
      transactionsCount: 1,
      totalAmount: -25000
    }
  ];
  analysis.counterAccounts = [
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    },
    {
      name: 'Jan Novák',
      appearances: [{ number: '000000-4776908073', bank_code: '0800', name: 'Danuše Nerudová' }],
      transactionsCount: 4,
      totalAmount: 120000
    }
  ];

  return analysis;
};

const getMedian = (transactions: Array<Transaction>): number | null => {
  if (transactions.length === 0) {
    return null;
  }
  // Sort transactions by amount
  const sorted: Array<Transaction> = transactions.sort(
    (a: Transaction, b: Transaction): number => a.amount - b.amount
  );
  const middle: number = Math.floor(sorted.length / 2);
  // If the number of transactions is odd, return the middle one
  if (sorted.length % 2) {
    return sorted[middle].amount;
  }
  // If the number of transactions is even, return the average of the two middle ones
  return (sorted[middle - 1].amount + sorted[middle].amount) / 2.0;
};
