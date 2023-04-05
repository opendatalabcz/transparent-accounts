import { Analysis, Transaction, TransactionsAggregation } from '../types';
import { format } from 'date-fns';

// TODO: REFACTOR, DOCUMENT AND TEST
export const analyse = (
  transactions: Array<Transaction>,
  balance: number | null,
  currency: string | null
): Analysis => {
  // Create an empty Analysis instance
  const analysis: Analysis = {
    currency: currency,
    transactionsCount: transactions.length,
    incomingCount: 0,
    outgoingCount: 0,
    balance: balance,
    incomingAmount: 0,
    outgoingAmount: 0,
    incomingAverage: null,
    outgoingAverage: null,
    incomingMedian: null,
    outgoingMedian: null,
    transparency: null,
    withDescription: null,
    identifiers: [],
    counterAccounts: [],
    dateAggregation: []
  };
  // Create auxiliary variables
  const incomingTransactions: Array<Transaction> = [];
  const outgoingTransactions: Array<Transaction> = [];
  let describableTransactionCount: number = 0;
  let transparentDescriptionCount: number = 0;
  let descriptionCount: number = 0;
  let currentBalance: number = balance || 0;
  let lastDate: string = format(new Date(), 'yyyy-MM-d');
  analysis.dateAggregation.push({
    date: lastDate,
    balance: currentBalance,
    incomingCount: 0,
    outgoingCount: 0
  });
  // Analyse
  transactions.forEach((transaction: Transaction) => {
    // Incoming x outgoing transactions + descriptions percentages
    if (transaction.type === 'INCOMING') {
      incomingTransactions.push(transaction);
      analysis.incomingAmount += transaction.amount;
    } else if (transaction.type === 'OUTGOING') {
      outgoingTransactions.push(transaction);
      analysis.outgoingAmount += transaction.amount;
      // Owner could have described the transaction
      if (
        transaction.type_detail !== 'Platba kartou' &&
        transaction.type_detail !== 'Výběr z bankomatu' &&
        transaction.type_detail !== 'Poplatek' &&
        transaction.type_detail !== 'Odvod daně'
      ) {
        describableTransactionCount++;
        transparentDescriptionCount =
          transaction.ca_name !== null
            ? transparentDescriptionCount + 1
            : transparentDescriptionCount;
        descriptionCount = transaction.description !== '' ? descriptionCount + 1 : descriptionCount;
      }
    }
    // Date aggregation
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
    // Identifiers aggregation
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
  // Set calculated values
  analysis.incomingCount = incomingTransactions.length;
  analysis.outgoingCount = outgoingTransactions.length;
  analysis.incomingAverage = analysis.incomingAmount / analysis.incomingCount;
  analysis.outgoingAverage = analysis.outgoingAmount / analysis.outgoingCount;
  analysis.incomingMedian = getMedian(incomingTransactions);
  analysis.outgoingMedian = getMedian(outgoingTransactions);
  analysis.transparency = transparentDescriptionCount / describableTransactionCount;
  analysis.withDescription = descriptionCount / describableTransactionCount;
  analysis.dateAggregation.reverse(); // Reverse the array
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
  // Empty array -> no median
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
