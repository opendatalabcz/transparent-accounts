interface Props {
  tab: 'transakce' | 'analyza';
  setTab: (tab: 'transakce' | 'analyza') => void;
}

function AccountSwitch({ tab, setTab }: Props): JSX.Element {
  return (
    <div className="d-flex justify-content-center">
      <button
        className={
          'tab-button tab-button-left px-3 py-2 ' + (tab === 'analyza' ? 'tab-button-active' : '')
        }
        onClick={() => setTab('analyza')}>
        Analýza 📈
      </button>
      <button
        className={
          'tab-button tab-button-right px-3 py-2 ' + (tab === 'transakce' ? 'tab-button-active' : '')
        }
        onClick={() => setTab('transakce')}>
        Výpis 💸
      </button>
    </div>
  );
}

export default AccountSwitch;
