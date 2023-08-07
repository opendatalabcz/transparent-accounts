export const formatAccNum = (acc: string, bankCode: string): string => {
  return `${shortenAccNum(acc)}/${bankCode}`;
};

export const shortenAccNum = (acc) => {
  // Remove leading zeros
  let withoutZeros = acc.replace(/^0+/, '');
  // Remove dash if it's starting character
  return withoutZeros.replace(/^-/, '');
};

export const getAccountLink = (acc: string, bankCode: string): string => {
  switch (bankCode) {
    case '0800':
      return `https://www.csas.cz/cs/transparentni-ucty#/${acc}`;
    case '0300':
      return `https://www.csob.cz/portal/firmy/bezne-ucty/transparentni-ucty/ucet?account=${shortenAccNum(
        acc
      )}`;
    case '2010':
      return `https://ib.fio.cz/ib/transparent?a=${getFioFormattedAccNum(acc)}`;
    case '0100':
      return `https://www.kb.cz/cs/transparentni-ucty/${getKBFormattedAccNum(acc)}`;
  }
  return '#';
};

const getFioFormattedAccNum = (acc: string): string => {
  // Remove the prefix
  let [, number] = acc.split('-');
  // Remove leading zeros in the number
  return number.replace(/^0+/, '');
};

const getKBFormattedAccNum = (acc: string): string => {
  // Split the account number into prefix and number
  let [prefix, number] = acc.split('-');
  // Remove leading zeros in the prefix
  prefix = prefix.replace(/^0+/, '');
  // Remove leading zeros in the number
  number = number.replace(/^0+/, '');
  // Return the formatted account number
  return prefix !== '' ? `${prefix}-${number}` : number;
};
