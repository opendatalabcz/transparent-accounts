export const formatAccNum = (acc: string, bankCode: string): string => {
  return `${shortenAccNum(acc)}/${bankCode}`;
}

export const shortenAccNum = (acc) => {
  // Remove leading zeros
  let withoutZeros = acc.replace(/^0+/, '');
  // Remove dash if it's starting character
  return withoutZeros.replace(/^-/, '');
};
