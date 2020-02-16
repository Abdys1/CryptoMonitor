class TransactionController {
  constructor(http) {
    this.http = http;
    this.url = "/api/transaction";
  }

  getUsersTransactions(pageNumber) {
    return new Promise((resolve, reject) => {
      this.http
        .get(this.url + `?page_num=${pageNumber}`)
        .then(response => resolve(response.data.hasOwnProperty("transactions") ? response.data["transactions"] : []))
        .catch(response => reject(response));
    });
  }

  updateTransaction(newTrans) {
    return new Promise((resolve, reject) => {
      this.http
        .put(this.url + newTrans.id, newTrans)
        .then(response => resolve(response.data))
        .catch(response => reject(response));
    });
  }
  //TODO Ha nem érvényes a tranzakció, akkor ne küldje el a szervernek

  deleteTransaction(transactions, deletedTransID) {
    return this.http.delete(this.url + deletedTransID).then(() => {
      let filtered = transactions.filter(function(value) {
        return value.id !== deletedTransID;
      });
      return filtered;
    });
  }

  saveTransaction(newTrans) {
    return new Promise((resolve, reject) => {
      this.http
        .post(this.url, newTrans)
        .then(response => resolve(response.data))
        .catch(response => reject(response));
    });
  }
}

export default TransactionController;
