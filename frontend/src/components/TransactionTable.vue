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
              v-if="
                props.item.date_of_sell == null || props.item.date_of_sell == ''
              "
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
              v-if="
                props.item.date_of_sell == null || props.item.date_of_sell == ''
              "
              v-model="props.item.quantity"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
      </template>
      <template v-slot:item.purchase_price="props">
        <v-edit-dialog :return-value.sync="props.item.amount">
          {{ props.item.purchase_price }}
          <template v-slot:input>
            <v-text-field
              v-if="
                props.item.date_of_sell == null || props.item.date_of_sell == ''
              "
              v-model="props.item.purchase_price"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
      </template>
      <template v-slot:item.action="props">
        <v-icon class="mr-2" small dark @click="openCloseDialog(props.item)">
          gavel
        </v-icon>
        <v-icon small dark @click="openDeleteDialog(props.item)">
          delete
        </v-icon>
      </template>
    </v-data-table>
    <DeleteDialog
      v-model="deleteDialog"
      :item="actualItem"
      @cancel="deleteDialog = false"
      @confirm="deleteTransaction"
    ></DeleteDialog>
    <CloseDialog
      v-model="closeDialog"
      :item="actualItem"
      @cancel="closeDialog = false"
      @confirm="closeTransaction"
    >
    </CloseDialog>
  </v-col>
</template>

<script>
import DeleteDialog from "./DeleteDialog";
import CloseDialog from "./CloseDialog";

export default {
  name: "TransactionTable",
  components: { CloseDialog, DeleteDialog },
  props: ["exchangeRate", "newTransaction"],
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Eladás dátuma", value: "date_of_sell" },
        { text: "Mennyiség", value: "quantity" },
        { text: "Árfolyam a vásárlás időpontjában", value: "purchase_price" },
        { text: "Nyereség %", value: "profit_percentage" },
        { text: "Nyereség $", value: "profit_usd" },
        { text: "Műveletek", value: "action" }
      ],
      deleteDialog: false,
      closeDialog: false,
      actualItem: null,
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
      let newTrans = this.createTransaction(trans);
      this.transactions.push(newTrans);
    },
    createTransaction: function(trans) {
      const profit = this.isClosedTransaction(trans)
        ? this.calcProfit(trans, trans.sell_price)
        : this.calcProfit(trans, this.exchangeRate);
      return {
        id: trans.id,
        date_of_purchase: new Date(trans.date_of_purchase).toISOString(),
        date_of_sell: trans.date_of_sell,
        quantity: trans.quantity,
        purchase_price: trans.purchase_price.toFixed(2),
        profit_percentage: profit.margin.toFixed(2),
        profit_usd: profit.profitInUSD.toFixed(2),
        owner: trans.owner
      };
    },
    isClosedTransaction: function(trans) {
      return (
        typeof trans.date_of_sell !== "undefined" &&
        typeof trans.sell_price !== "undefined"
      );
    },
    calcProfit: function(trans, exchangeRate) {
      const floatQuantity = parseFloat(trans.quantity);
      const floatPurchasePrice = parseFloat(trans.purchase_price);
      const floatExchangeRate = parseFloat(exchangeRate);

      const profitInUSD =
        floatQuantity * floatExchangeRate - floatQuantity * floatPurchasePrice;
      const margin = (profitInUSD / (floatQuantity * floatExchangeRate)) * 100;
      return {
        profitInUSD: profitInUSD,
        margin: margin
      };
    },
    updateRow: function(item) {
      const newTrans = this.buildTransaction(item);
      this.$transAPI
        .updateTransaction(newTrans)
        .catch(response => window.console.log(response));
    },
    openCloseDialog: function(item) {
      this.actualItem = item;
      this.closeDialog = true;
    },
    closeTransaction: function(dateOfSell, sellPrice) {
      let newTrans = this.buildTransaction(this.actualItem);
      newTrans.date_of_sell = dateOfSell;
      newTrans.sell_price = sellPrice;
      this.$transAPI
        .updateTransaction(newTrans)
        .then(() => {
          this.actualItem.date_of_sell = dateOfSell;
          this.closeDialog = false;
        })
        .catch(response => window.console.log(response));
    },
    buildTransaction: function(item) {
      return {
        id: item.id,
        quantity: item.quantity,
        date_of_purchase: new Date(item.date_of_purchase),
        purchase_price: item.purchase_price,
        owner: item.owner
      };
    },
    openDeleteDialog: function(item) {
      this.actualItem = item;
      this.deleteDialog = true;
    },
    deleteTransaction: async function() {
      this.transactions = await this.$transAPI.deleteTransaction(
        this.transactions,
        this.actualItem.id
      );
      this.deleteDialog = false;
    }
  },
  watch: {
    exchangeRate: function(newExRate) {
      this.transactions.forEach(trans => {
        if (trans.date_of_sell === undefined) {
          let profit = this.calcProfit(trans, newExRate);
          trans.profit_usd = profit.profitInUSD.toFixed(2);
          trans.profit_percentage = profit.margin.toFixed(2);
        }
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
