<template>
  <v-data-table :headers="headers" :items="transactions" class="elevation-1">
    <template v-slot:item.date_of_purchase="props">
      <v-edit-dialog :return-value.sync="props.item.date_of_purchase">
        {{ props.item.date_of_purchase }}
        <template v-slot:input>
          <v-text-field
            v-model="props.item.date_of_purchase"
            label="Szerkesztés"
            single-line
            counter
          ></v-text-field>
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.date_of_sell="props">
      <v-edit-dialog :return-value.sync="props.item.date_of_sell">
        {{ props.item.date_of_sell }}
        <template v-slot:input>
          <v-text-field
            v-model="props.item.date_of_sell"
            label="Szerkesztés"
            single-line
            counter
          ></v-text-field>
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.quantity="props">
      <v-edit-dialog :return-value.sync="props.item.quantity">
        {{ props.item.quantity }}
        <template v-slot:input>
          <v-text-field
            v-model="props.item.quantity"
            label="Szerkesztés"
            single-line
            counter
          ></v-text-field>
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.amount="props">
      <v-edit-dialog :return-value.sync="props.item.amount">
        {{ props.item.amount }}
        <template v-slot:input>
          <v-text-field
            v-model="props.item.amount"
            label="Szerkesztés"
            single-line
            counter
          ></v-text-field>
        </template>
      </v-edit-dialog>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: "TransactionTable",
  props: ["exchangeRate", "newTransaction"],
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Eladás dátuma", value: "date_of_sell" },
        { text: "Mennyiség", value: "quantity" },
        { text: "Árfolyam a vásárlás időpontjában", value: "amount" },
        { text: "Nyereség %", value: "profit_percentage" },
        { text: "Nyereség $", value: "profit_usd" }
      ],
      transactions: []
    };
  },
  methods: {
    getUsersTransactions: function() {
      return new Promise((resolve, reject) => {
        this.$http
          .get("/api/transaction/")
          .then(response => resolve(response.data))
          .catch(response => reject(response));
      });
    },
    initTransactions: function() {
      this.getUsersTransactions()
        .then(items => {
          items.forEach(trans => {
            this.addNewTransaction(trans);
          });
        })
        .catch(response => window.console.log(response));
    },
    addNewTransaction: function(trans) {
      const newTrans = this.createTransaction(trans);
      this.transactions.push(newTrans);
    },
    createTransaction: function(trans) {
      const profitUSD = this.profitInUSD(trans.quantity, trans.purchase_price);
      const profitPercentage = this.profitPercentage(trans.quantity, profitUSD);
      return {
        date_of_purchase: new Date(trans.date_of_purchase).toLocaleString(),
        date_of_sell: trans.date_of_sell,
        quantity: trans.quantity,
        amount: trans.purchase_price.toFixed(2),
        profit_percentage: profitPercentage.toFixed(2),
        profit_usd: profitUSD.toFixed(2)
      };
    },
    profitInUSD: function(quantity, purchasePrice) {
      return quantity * this.exchangeRate - quantity * purchasePrice;
    },
    profitPercentage: function(quantity, profitUSD) {
      return (profitUSD / (quantity * this.exchangeRate)) * 100;
    },
    save: function() {},
    close: function() {},
    open: function() {},
    cancel: function() {}
  },
  watch: {
    exchangeRate: function() {
      this.transactions.forEach(trans => {
        const profitUSD = this.profitInUSD(trans.quantity, trans.amount);
        const profitPercentage = this.profitPercentage(
          trans.quantity,
          profitUSD
        );
        trans.profit_usd = profitUSD.toFixed(2);
        trans.profit_percentage = profitPercentage.toFixed(2);
      });
    },
    newTransaction: function(trans) {
      this.addNewTransaction(trans);
    }
  },
  mounted() {
    this.initTransactions();
  }
};
</script>

<style scoped></style>
