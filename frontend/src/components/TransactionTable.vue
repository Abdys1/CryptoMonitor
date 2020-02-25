<template>
  <v-col>
    <v-data-table
      :headers="headers"
      :items="transactions"
      :items-per-page="numberOfItems"
      :loading="loading"
      loading-text="Kis türelmet..."
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
      <template v-slot:item.buy_amount="props">
        <v-edit-dialog
          :return-value.sync="props.item.buy_amount"
          v-if="!isClosedTransaction(props.item)"
        >
          {{ props.item.buy_amount }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.buy_amount"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
              single-line
              counter
            ></v-text-field>
          </template>
        </v-edit-dialog>
        <span v-if="isClosedTransaction(props.item)">{{
          props.item.buy_amount
        }}</span>
      </template>
      <template v-slot:item.profit_percentage="props">
        <v-chip :color="getColor(props.item)">{{
          props.item.profit_percentage
        }}</v-chip>
      </template>
      <template v-slot:item.profit_usd="props">
        <v-chip :color="getColor(props.item)">{{
          props.item.profit_usd
        }}</v-chip>
      </template>
      <template v-slot:item.action="props">
        <TransactionCloseButton
          :exchange-rate="exchangeRate"
          :trans="props.item"
          @transClosed="initTransactions"
        >
        </TransactionCloseButton>
        <TransactionDeleteButton
          :trans-id="props.item.id"
          @transDeleted="initTransactions"
        >
        </TransactionDeleteButton>
      </template>
    </v-data-table>

    <div class="text-center pt-2">
      <v-pagination
        v-model="page"
        :length="pageCount"
        :total-visible="6"
        dark
      ></v-pagination>
    </div>
  </v-col>
</template>

<script>
import formatter from "./util/DateFormatter";
import calcProfit from "./util/ProfitCalculator";
import TransactionDeleteButton from "./TransactionDeleteButton";
import Transaction from "./util/Transaction";
import TransactionCloseButton from "./TransactionCloseButton";

export default {
  name: "TransactionTable",
  components: {TransactionCloseButton, TransactionDeleteButton},
  props: { exchangeRate: Number, newTransaction: Object },
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Értékesítés dátuma", value: "date_of_sell" },
        { text: "Árfolyam a vásárlás időpontjában", value: "purchase_price" },
        { text: "Elköltött összeg $", value: "buy_amount" },
        { text: "Mennyiség", value: "quantity" },
        { text: "Árfolyam az értékesítés időpontjában", value: "sell_price" },
        { text: "Jelenlegi összeg $", value: "sell_amount" },
        { text: "Haszonkulcs", value: "profit_percentage" },
        { text: "Nyereség", value: "profit_usd" },
        { text: "Műveletek", value: "action" }
      ],
      numberOfItems: 10,
      page: 1,
      loading: false,
      pageCount: 0,
      prevPurchaseDate: null,
      transactions: []
    };
  },
  methods: {
    initTransactions: function() {
      this.transactions = [];
      this.loading = true;
      this.$transAPI
        .getUsersTransactions(this.page)
        .then(response => {
          this.pageCount = response["pageCount"];
          let transactions = response["transactions"];
          transactions.forEach(trans => {
            this.addNewTransaction(trans);
          });
          this.loading = false;
        })
        .catch(() => (this.loading = false));
    },
    addNewTransaction: function(trans) {
      let newTrans = this.createTransaction(trans);
      this.transactions.push(newTrans);
    },
    createTransaction: function(trans) {
      const profit = this.isClosedTransaction(trans)
        ? calcProfit(trans, trans.sell_price)
        : calcProfit(trans, this.exchangeRate);

      return {
        id: trans.id,
        date_of_purchase: formatter.getPrettyDate(
          new Date(trans.date_of_purchase)
        ),
        date_of_sell: trans.hasOwnProperty("date_of_sell")
          ? formatter.getPrettyDate(new Date(trans.date_of_sell))
          : "",
        quantity: trans.quantity,
        buy_amount: trans.buy_amount,
        purchase_price: trans.buy_amount / trans.quantity,
        sell_price: trans.sell_price,
        sell_amount: this.getCurrentAmount(trans),
        profit_percentage: profit.markup,
        profit_usd: profit.profitInUSD,
        owner: trans.owner
      };
    },
    getCurrentAmount: function(trans) {
      return "sell_price" in trans
        ? trans.quantity * trans.sell_price
        : trans.quantity * this.exchangeRate;
    },
    isClosedTransaction: function(trans) {
      return !!trans.date_of_sell && !!trans.sell_price;
    },
    updateRow: function(item) {
      const newTrans = new Transaction(item);
      this.$transAPI
        .updateTransaction(newTrans)
        .catch(response => window.console.log(response));
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
    },
    getColor: function(item) {
      return item.profit_percentage > 0 ? "green" : "red";
    }
  },
  watch: {
    exchangeRate: function(newExRate) {
      this.transactions.forEach(trans => {
        if (trans.date_of_sell === "") {
          trans.sell_amount = trans.quantity * this.exchangeRate;
          let profit = calcProfit(trans, newExRate);
          trans.profit_usd = profit.profitInUSD;
          trans.profit_percentage = profit.markup;
        }
      });
    },
    newTransaction: function(trans) {
      if (this.numberOfItems > this.transactions.length) {
        this.addNewTransaction(trans);
      } else {
        this.pageCount += 1;
        this.page += 1;
      }
    },
    page: function() {
      this.initTransactions();
    }
  },
  mounted() {
    this.initTransactions();
  }
};
</script>

<style scoped></style>
