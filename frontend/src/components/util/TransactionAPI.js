class TransactionController {
  constructor(http) {
    this.http = http;
    this.url = "/api/transaction";
  }

  getUsersTransactions(pageNumber, itemPerPage) {
    return new Promise((resolve, reject) => {
      this.http
        .get(this.url + `?page_num=${pageNumber}&item_per_page=${itemPerPage}`)
        .then(response => {
          if (
            response.data.hasOwnProperty("transactions") &&
            response.data.hasOwnProperty("pageCount")
          )
            resolve(response.data);
          else reject("Cannot fetch data!");
        })
        .catch(response => reject(response));
    });
  }

  updateTransaction(newTrans) {
    return new Promise((resolve, reject) => {
      this.http
        .put(this.url + `\\${newTrans.id}`, newTrans)
        .then(response => resolve(response.data))
        .catch(response => reject(response));
    });
  }
  //TODO Ha nem érvényes a tranzakció, akkor ne küldje el a szervernek

  deleteTransaction(deletedTransID) {
    // return this.http.delete(this.url + `\\${deletedTransID}`).then(() => {
    //   let filtered = transactions.filter(function(value) {
    //     return value.id !== deletedTransID;
    //   });
    //   return filtered;
    // });
    return new Promise((resolve, reject) => {
      this.http
        .delete(this.url + `\\${deletedTransID}`)
        .then(response => resolve(response))
        .catch(err => reject(err));
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
