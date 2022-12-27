from app.models import Account, Transaction


def json_encode(o):
    match o:
        case Account():
            return {
                "number": o.number,
                "bank_code": o.bank_code,
                "name": o.name,
                "owner": o.owner,
                "balance": o.balance,
                "currency": o.currency.name,
                "description": o.description,
                "created": o.created,
                "last_updated": o.last_updated,
                "last_fetched": o.last_fetched,
                "archived": o.archived,
                "transactions": o.transactions
            }
        case Transaction():
            return {
                "date": o.date,
                "amount": o.amount,
                "counter_account": o.counter_account,
                "type": o.type.name,
                "type_detail": o.str_type,
                "variable_symbol": o.variable_symbol,
                "constant_symbol": o.constant_symbol,
                "specific_symbol": o.specific_symbol,
                "description": o.description
            }
        case _:
            return str(o)
