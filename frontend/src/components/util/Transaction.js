function Transaction(tableItem) {
  return {
    id: tableItem.id,
    quantity: parseFloat(tableItem.quantity),
    date_of_purchase: new Date(tableItem.date_of_purchase),
    buy_amount: parseFloat(tableItem.buy_amount),
    owner: tableItem.owner
  };
}

export default Transaction;
