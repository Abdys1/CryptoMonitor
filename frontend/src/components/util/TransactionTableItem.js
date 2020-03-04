import formatter from './DateFormatter'
import calcProfit from "./ProfitCalculator";

class TransactionTableItem {
  constructor(trans, actualExchangeRate) {
    const profit =
      "date_of_sell" in trans
        ? calcProfit(trans, trans.sell_price)
        : calcProfit(trans, actualExchangeRate);

    this.id = trans.id;
    this.date_of_purchase = formatter.getPrettyDate(
      new Date(trans.date_of_purchase)
    );
    this.date_of_sell =
      "date_of_sell" in trans
        ? formatter.getPrettyDate(new Date(trans.date_of_sell))
        : "";
    this.quantity = trans.quantity;
    this.buy_amount = trans.buy_amount;
    this.purchase_price = trans.buy_amount / trans.quantity;
    this.sell_price = "sell_price" in trans ? trans.sell_price : "";
    this.sell_amount = this.getCurrentAmount(trans, actualExchangeRate);
    this.profit_percentage = profit.markup;
    this.profit_usd = profit.profitInUSD;
    this.owner = trans.owner;
  }

  getCurrentAmount(trans, exchangeRate) {
    return "sell_price" in trans
      ? trans.quantity * trans.sell_price
      : trans.quantity * exchangeRate;
  }

  isClosedTransaction() {
    return !!this.date_of_sell && !!this.sell_price;
  }
}

export default TransactionTableItem;