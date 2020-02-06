<template>
  <v-col>
    <v-data-table
      :headers="headers"
      :items="transactions"
      class="second elevation-1"
    >
      <template v-slot:item.date_of_purchase="props">
        <v-edit-dialog :return-value.sync="props.item.date_of_purchase">
          {{ props.item.date_of_purchase }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.date_of_purchase"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
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
              @keyup.enter="updateRow(props.item)"
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
              @keyup.enter="updateRow(props.item)"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
      </template>
      <template v-slot:item.action="props">
        <v-icon class="mr-2" small dark @click="closeTransaction(props.item)">
          gavel
        </v-icon>
        <v-icon small dark @click="deleteTransaction(props.item)">
          delete
        </v-icon>
      </template>
    </v-data-table>
  </v-col>
</template>

<script>
export default {
  name: "TransactionTable",
  components: {},
  props: ["exchangeRate", "newTransaction"],
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Eladás dátuma", value: "date_of_sell" },
        { text: "Mennyiség", value: "quantity" },
        { text: "Árfolyam a vásárlás időpontjában", value: "amount" },
        { text: "Nyereség %", value: "profit_percentage" },
        { text: "Nyereség $", value: "profit_usd" },
        { text: "Műveletek", value: "action" }
      ],
      transactions: []
    };
  },
  methods: {
    initTransactions: function() {
      this.$transAPI
        .getUsersTransactions()
        .then(items => {
          items.forEach(trans => {
            this.addNewTransaction(trans);
          });
        })
        .catch(response => window.console.log(response));
    },
    addNewTransaction: function(trans) {
      const newTrans = this.createReactiveTransaction(trans);
      this.transactions.push(newTrans);
    },
    createReactiveTransaction: function(trans) {
      const profitUSD = this.profitInUSD(trans.quantity, trans.purchase_price);
      const profitPercentage = this.profitPercentage(trans.quantity, profitUSD);
      return {
        id: trans.id,
        date_of_purchase: new Date(trans.date_of_purchase).toISOString(),
        date_of_sell: trans.date_of_sell,
        quantity: trans.quantity,
        amount: trans.purchase_price.toFixed(2),
        profit_percentage: profitPercentage.toFixed(2),
        profit_usd: profitUSD.toFixed(2),
        owner: trans.owner
      };
    },
    profitInUSD: function(quantity, purchasePrice) {
      return quantity * this.exchangeRate - quantity * purchasePrice;
    },
    profitPercentage: function(quantity, profitUSD) {
      return (profitUSD / (quantity * this.exchangeRate)) * 100;
    },
    updateRow: function(item) {
      const newTrans = this.buildTransaction(item);
      this.$transAPI
        .updateTransaction(newTrans)
        .catch(response => window.console.log(response));
    },
    closeTransaction: function(item) {
      let options = {
        okText: "Lezárás",
        cancelText: "Mégse"
      };

      this.$dialog
        .confirm("Biztosan le szeretnéd zárni ezt a tranzakciót?", options)
        .then(() => {
          const dateOfSell = new Date();
          let newTrans = this.buildTransaction(item);
          newTrans.date_of_sell = dateOfSell;
          this.$transAPI
            .updateTransaction(newTrans)
            .then(() => (item.date_of_sell = dateOfSell))
            .catch(response => window.console.log(response));
        });
    },
    buildTransaction: function(item) {
      return {
        id: item.id,
        quantity: item.quantity,
        date_of_purchase: new Date(item.date_of_purchase),
        purchase_price: item.amount,
        owner: item.owner
      };
    },
    deleteTransaction: function(item) {
      let options = {
        okText: "Törlés",
        cancelText: "Mégse"
      };

      this.$dialog
        .confirm("Biztosan törölni szeretnéd a tranzakciót?", options)
        .then(async () => {
          this.transactions = await this.$transAPI.deleteTransaction(
            this.transactions,
            item.id
          );
        });
    }
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
