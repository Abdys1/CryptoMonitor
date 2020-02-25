function calcProfit(trans, exchangeRate) {
    let currentAmount = trans.quantity * exchangeRate;
    let profit = currentAmount - trans.buy_amount;
    let markup = profit / trans.buy_amount * 100
    return {
        profitInUSD: parseFloat(profit.toFixed(2)),
        markup: parseFloat(markup.toFixed(2))
    }
}

export default calcProfit;
