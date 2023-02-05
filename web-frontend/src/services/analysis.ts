import { Analysis, TransactionsAggregation, Transaction } from '../types';
import { format } from 'date-fns';

// TODO REFACTOR AND DOCUMENT!
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
  analysis.identifiers = [];
  analysis.counterAccounts = [];

  // Create auxiliary variables
  const incomingTransactions: Array<Transaction> = [];
  const outgoingTransactions: Array<Transaction> = [];
  let describableTransactionCount: number = 0;
  let transparentDescriptionCount: number = 0;
  let descriptionCount: number = 0;
  // Calculate first set of values
  transactions.forEach((transaction: Transaction) => {
    if (transaction.type === 'INCOMING') {
      incomingTransactions.push(transaction);
      analysis.incomingAmount += transaction.amount;
    } else if (transaction.type === 'OUTGOING') {
      outgoingTransactions.push(transaction);
      // Owner could have described the transaction
      if (
        transaction.category !== 'Platba kartou' &&
        transaction.category !== 'Výběr z bankomatu' &&
        transaction.category !== 'Poplatek' &&
        transaction.category !== 'Odvod daně'
      ) {
        describableTransactionCount++;
        transparentDescriptionCount =
          transaction.ca_name !== null
            ? transparentDescriptionCount + 1
            : transparentDescriptionCount;
        descriptionCount = transaction.description !== '' ? descriptionCount + 1 : descriptionCount;
      }
      analysis.outgoingAmount += transaction.amount;
    }
  });
  // Set calculated values
  analysis.incomingCount = incomingTransactions.length;
  analysis.outgoingCount = outgoingTransactions.length;
  analysis.incomingAverage = analysis.incomingAmount / analysis.incomingCount;
  analysis.outgoingAverage = analysis.outgoingAmount / analysis.outgoingCount;
  analysis.incomingMedian = getMedian(incomingTransactions);
  analysis.outgoingMedian = getMedian(outgoingTransactions);
  analysis.transparency = transparentDescriptionCount / describableTransactionCount;
  analysis.withDescription = descriptionCount / describableTransactionCount;

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

  // Calculate third set of values
  transactions.forEach((transaction: Transaction) => {
    if (
      transaction.type === 'OUTGOING' &&
      transaction.ca_identifier !== null &&
      transaction.ca_name !== null
    ) {
      const identifier: TransactionsAggregation | undefined = analysis.identifiers.find(
        (a: TransactionsAggregation) => a.name === transaction.ca_name
      );
      if (identifier) {
        identifier.transactionsCount++;
        identifier.totalAmount += transaction.amount;
      } else {
        analysis.identifiers.push({
          name: transaction.ca_name,
          identifier: transaction.ca_identifier,
          transactionsCount: 1,
          totalAmount: transaction.amount,
          currency: transaction.currency
        });
      }
    }
    if (transaction.type === 'INCOMING' && transaction.counter_account !== null) {
      const counter_account: TransactionsAggregation | undefined = analysis.counterAccounts.find(
        (a: TransactionsAggregation) => a.name === transaction.counter_account
      );
      if (counter_account) {
        counter_account.transactionsCount++;
        counter_account.totalAmount += transaction.amount;
      } else {
        analysis.counterAccounts.push({
          name: transaction.counter_account,
          transactionsCount: 1,
          totalAmount: transaction.amount,
          currency: transaction.currency
        });
      }
    }
  });
  // Sort by total amount
  analysis.identifiers.sort(
    (a: TransactionsAggregation, b: TransactionsAggregation): number =>
      a.totalAmount - b.totalAmount
  );
  analysis.counterAccounts.sort(
    (a: TransactionsAggregation, b: TransactionsAggregation): number =>
      b.totalAmount - a.totalAmount
  );

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
