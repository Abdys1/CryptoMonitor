class ProfitCalculator {
    constructor(trans) {
        this.quantity = parseFloat(trans.quantity);
        this.purchasePrice = parseFloat(trans.purchase_price);
    }


}

export default ProfitCalculator;