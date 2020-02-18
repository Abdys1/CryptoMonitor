<template>
  <v-col>
    <v-data-table
      :headers="headers"
      :items="transactions"
      :items-per-page="numberOfItems"
      hide-default-footer
      class="second elevation-1"
    >
      <template v-slot:no-data>
        Még nincs egyetlen aktív tranzakciód sem!
      </template>
      <template v-slot:item.date_of_purchase="props">
        <v-edit-dialog
          v-if="!isClosedTransaction(props.item)"
          large
          persistent
          save-text="Mentés"
          cancel-text="Bezár"
          @open="savePrevDateTime(props.item)"
          @save="updateRow(props.item)"
          @cancel="restorePrevPurchaseDate(props.item)"
        >
          {{ props.item.date_of_purchase }}
          <template v-slot:input>
            <v-datetime-picker
              label="Értékesítés időpontja"
              v-model="props.item.date_of_purchase"
              @input="formatDateTime($event, props.item)"
            >
              <template slot="actions" slot-scope="{ parent }">
                <v-btn color="success darken-1" @click="parent.okHandler()"
                  >Rendben</v-btn
                >
              </template>
            </v-datetime-picker>
          </template>
        </v-edit-dialog>
        <span v-if="isClosedTransaction(props.item)">{{
          props.item.date_of_sell
        }}</span>
      </template>
      <template v-slot:item.quantity="props">
        <v-edit-dialog
          :return-value.sync="props.item.quantity"
          v-if="!isClosedTransaction(props.item)"
        >
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
        <span v-if="isClosedTransaction(props.item)">{{
          props.item.quantity
        }}</span>
      </template>
      <template v-slot:item.purchase_price="props">
        <v-edit-dialog
          :return-value.sync="props.item.purchase_price"
          v-if="!isClosedTransaction(props.item)"
        >
          {{ props.item.purchase_price }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.purchase_price"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
        <span v-if="isClosedTransaction(props.item)">{{
          props.item.purchase_price
        }}</span>
      </template>
      <template v-slot:item.action="props">
        <v-icon
          class="mr-2"
          small
          dark
          @click="openTransactionCloserDialog(props.item)"
        >
          gavel
        </v-icon>
        <v-icon small dark @click="openDeleteDialog(props.item)">
          delete
        </v-icon>
      </template>
    </v-data-table>
    <div class="text-center pt-2">
      <v-pagination
        v-model="page"
        :length="pageCount"
        @next="initTransactions()"
        @previous="initTransactions()"
        @input="initTransactions()"
        dark
      ></v-pagination>
    </div>
    <DeleteDialog
      v-model="deleteDialog"
      :item="actualItem"
      @cancel="deleteDialog = false"
      @confirm="deleteTransaction"
    ></DeleteDialog>
    <CloseDialog
      v-model="closeDialog"
      :key="componentKey"
      :actual-exchange-rate="exchangeRate"
      @cancel="closeDialog = false"
      @confirm="closeTransaction"
    >
    </CloseDialog>
  </v-col>
</template>

<script>
import DeleteDialog from "./dialogs/DeleteDialog";
import CloseDialog from "./dialogs/CloseDialog";
import formatter from "./util/DateFormatter";

export default {
  name: "TransactionTable",
  components: { CloseDialog, DeleteDialog },
  props: { exchangeRate: Number, newTransaction: Object },
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Eladás dátuma", value: "date_of_sell" },
        { text: "Mennyiség", value: "quantity" },
        { text: "Árfolyam a vásárlás időpontjában", value: "purchase_price" },
        { text: "Árfolyam az értékesítés időpontjában", value: "sell_price" },
        { text: "Nyereség %", value: "profit_percentage" },
        { text: "Nyereség $", value: "profit_usd" },
        { text: "Műveletek", value: "action" }
      ],
      deleteDialog: false,
      closeDialog: false,
      actualItem: null,
      componentKey: 0,
      numberOfItems: 10,
      page: 1,
      pageCount: 0,
      prevPurchaseDate: null,
      transactions: []
    };
  },
  methods: {
    initTransactions: function() {
      this.transactions = [];
      this.$transAPI
        .getUsersTransactions(this.page)
        .then(response => {
          this.pageCount = response["pageCount"];
          let transactions = response["transactions"];
          transactions.forEach(trans => {
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
        date_of_purchase: formatter.getPrettyDate(
          new Date(trans.date_of_purchase)
        ),
        date_of_sell: trans.hasOwnProperty("date_of_sell")
          ? formatter.getPrettyDate(new Date(trans.date_of_sell))
          : undefined,
        quantity: trans.quantity,
        purchase_price: trans.purchase_price.toFixed(2),
        sell_price: trans.hasOwnProperty("sell_price")
          ? trans.sell_price.toFixed(2)
          : undefined,
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
    openTransactionCloserDialog: function(item) {
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
          this.closeActualItem(dateOfSell, sellPrice);
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
    closeActualItem: function(dateOfSell, sellPrice) {
      const profit = this.calcProfit(
        this.actualItem,
        this.actualItem.sell_price
      );

      this.actualItem.date_of_sell = formatter.getPrettyDate(dateOfSell);
      this.actualItem.sell_price = sellPrice.toFixed(2);
      this.actualItem.profit_usd = profit.profitInUSD.toFixed(2);
      this.actualItem.profit_percentage = profit.margin.toFixed(2);
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
    },
    formatDateTime: function(datetime, item) {
      item.date_of_purchase = formatter.getPrettyDate(datetime);
    },
    savePrevDateTime: function(item) {
      this.prevPurchaseDate = item.date_of_purchase;
    },
    restorePrevPurchaseDate: function(item) {
      item.date_of_purchase = formatter.getPrettyDate(
        new Date(this.prevPurchaseDate)
      );
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
      if (this.numberOfItems > this.transactions.length) {
        this.addNewTransaction(trans);
      }
    },
    closeDialog: function() {
      if (this.closeDialog === true) {
        this.componentKey += 1;
      }
    }
  },
  mounted() {
    this.initTransactions();
  }
};
</script>

<style scoped></style>
