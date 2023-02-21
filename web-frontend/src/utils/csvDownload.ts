import { format } from 'date-fns';
import { Transaction } from '../types';

/**
 * Convert a Transaction array into a CSV string.
 */
export const transactionToCSV = (data: Array<Transaction>) => {
  const header: Array<String> = [
    'Datum',
    'Částka',
    'Měna',
    'Typ',
    'Protiúčet',
    'VS',
    'KS',
    'SS',
    'Poznámka',
    'IČO',
    'Společnost',
    'Kategorie'
  ];

  const rows = data
    .map(
      (t: Transaction): string =>
        [
          format(new Date(t.date), 'dd.MM.yyyy'),
          t.amount.toLocaleString('cs-CZ', {
            maximumFractionDigits: 2
          }),
          t.currency,
          t.type_detail.replaceAll('"', '""'), // Escape double quotes,
          t.counter_account != null ? t.counter_account.replaceAll('"', '""') : null, // Escape double quotes
          t.variable_symbol,
          t.constant_symbol,
          t.specific_symbol,
          t.description.replaceAll('"', '""'), // Escape double quotes
          t.ca_identifier,
          t.ca_name != null ? t.ca_name.replaceAll('"', '""') : null, // Escape double quotes,
          t.category
        ]
          .map((v: string | null) => (v ? `"${v}"` : '')) // Quote values
          .join(',') // Comma-separated
    )
    .join('\r\n'); // Rows starting on new lines

  // Return header and rows
  return [header.join(','), rows].join('\r\n');
};

/**
 * Download contents as a file.
 * Source: https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side
 */
export const downloadBlob = (content: string, filename: string, contentType: string) => {
  // Create a blob
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);

  // Create a link to download it
  const pom = document.createElement('a');
  pom.href = url;
  pom.setAttribute('download', filename);
  pom.click();
};
