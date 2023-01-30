import { Analysis, Transaction } from '../types';

export const analyse = (
  transactions: Array<Transaction>,
  balance: number | null,
  currency: string | null
): Analysis => {
  const analysis: Analysis = {} as Analysis;
  analysis.currency = currency;
  const incomingTransactions: Array<Transaction> = [];
  const outgoingTransactions: Array<Transaction> = [];
  analysis.incomingAmount = 0;
  analysis.outgoingAmount = 0;
  let transparentNoteCount: number = 0;
  let noteCount: number = 0;

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

  analysis.transactionsCount = transactions.length;
  analysis.incomingCount = incomingTransactions.length;
  analysis.outgoingCount = outgoingTransactions.length;
  analysis.balance = balance;
  analysis.incomingAverage = analysis.incomingAmount / analysis.incomingCount;
  analysis.outgoingAverage = analysis.outgoingAmount / analysis.outgoingCount;
  analysis.incomingMedian = getMedian(incomingTransactions);
  analysis.outgoingMedian = getMedian(outgoingTransactions);
  analysis.transparency = transparentNoteCount / analysis.outgoingCount;
  analysis.noted = noteCount / analysis.outgoingCount;

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
