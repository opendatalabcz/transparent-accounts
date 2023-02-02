import { useNavigate } from 'react-router-dom';

export const useAccountNavigate = () => {
  const navigate = useNavigate();

  return (accountNumber: string, bankCode: string): void => {
    navigate(`/ucty/${bankCode}/${accountNumber}`);
  };
};
