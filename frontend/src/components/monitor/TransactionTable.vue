<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="transactions"
      :loading="loading"
      loading-text="Kis türelmet..."
      hide-default-footer
      class="second box"
    >
      <template v-slot:no-data>
        Még nincs egyetlen aktív tranzakciód sem!
      </template>
      <template v-slot:item.date_of_purchase="props">
        <v-edit-dialog
          v-if="!props.item.isClosedTransaction()"
          large
          persistent
          save-text="Mentés"
          cancel-text="Bezár"
          @open="prevPurchaseDate = props.item.date_of_purchase"
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
        <span v-if="props.item.isClosedTransaction()">{{
          props.item.date_of_sell
        }}</span>
      </template>
      <template v-slot:item.quantity="props">
        <v-edit-dialog
          :return-value.sync="props.item.quantity"
          v-if="!props.item.isClosedTransaction()"
        >
          {{ parseFloat(props.item.quantity).toFixed(6) + " BTC" }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.quantity"
              label="Szerkesztés"
              @keyup.enter="updateRow(props.item)"
              single-line
            ></v-text-field>
          </template>
        </v-edit-dialog>
        <span v-if="props.item.isClosedTransaction()">{{
          parseFloat(props.item.quantity).toFixed(6) + " BTC"
        }}</span>
      </template>
      <template v-slot:item.buy_amount="props">
        <v-edit-dialog
          :return-value.sync="props.item.buy_amount"
          v-if="!props.item.isClosedTransaction()"
        >
          {{ parseFloat(props.item.buy_amount).toFixed(2) }}
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
        <span v-if="props.item.isClosedTransaction()">{{
          props.item.buy_amount.toFixed(2)
        }}</span>
      </template>
      <template v-slot:item.profit_percentage="props">
        <v-chip :color="getColor(props.item)">{{
          parseFloat(props.item.profit_percentage).toFixed(2) + "%"
        }}</v-chip>
      </template>
      <template v-slot:item.profit_usd="props">
        <v-chip :color="getColor(props.item)">{{
          parseFloat(props.item.profit_usd).toFixed(2) + " $"
        }}</v-chip>
      </template>
      <template v-slot:item.sell_amount="props">
        {{ props.item.sell_amount.toFixed(2) }}
      </template>
      <template v-slot:item.purchase_price="props">
        {{ parseFloat(props.item.purchase_price).toFixed(2) }}
      </template>
      <template v-slot:item.sell_price="props">
        <span v-if="props.item.isClosedTransaction()">
          {{ parseFloat(props.item.sell_price).toFixed(2) }}
        </span>
      </template>
      <template v-slot:item.action="props">
        <div class="operations">
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
        </div>
      </template>
    </v-data-table>

    <div class="text-center pt-2" style="display: flex">
      <v-pagination
        v-model="page"
        :length="pageCount"
        :total-visible="6"
        dark
      ></v-pagination>
      <v-text-field
        :value="numberOfItems"
        label="Megjelenített tranzakciók"
        type="number"
        min="-1"
        max="15"
        @input="numberOfItems = parseInt($event, 10)"
        @keydown.enter="changeItemsPerPage"
        class="itemNumberSelector"
      ></v-text-field>
    </div>
  </div>
</template>

<script>
import formatter from "../util/DateFormatter";
import calcProfit from "../util/ProfitCalculator";
import TransactionDeleteButton from "./TransactionDeleteButton";
import Transaction from "../util/Transaction";
import TransactionCloseButton from "./TransactionCloseButton";
import TransactionTableItem from "../util/TransactionTableItem";

export default {
  name: "TransactionTable",
  components: {
    TransactionCloseButton,
    TransactionDeleteButton
  },
  props: { exchangeRate: Number, newTransaction: Object },
  data: function() {
    return {
      headers: [
        { text: "Vásárlás dátuma", value: "date_of_purchase" },
        { text: "Értékesítés dátuma", value: "date_of_sell" },
        {
          text: "Árfolyam a vásárlás időpontjában (USDT)",
          value: "purchase_price"
        },
        { text: "Elköltött összeg (USDT)", value: "buy_amount" },
        { text: "Mennyiség (BTC)", value: "quantity" },
        {
          text: "Árfolyam az értékesítés időpontjában (USDT)",
          value: "sell_price"
        },
        { text: "Jelenlegi összeg (USDT)", value: "sell_amount" },
        { text: "Nyereség (USDT)", value: "profit_usd" },
        { text: "Haszonkulcs %", value: "profit_percentage" },
        { text: "Műveletek", value: "action" }
      ],
      numberOfItems: 10,
      page: 1,
      loading: false,
      pageCount: 0,
      prevPurchaseDate: null,
      transactions: [],
      statisticKey: 0,
      type: "open"
    };
  },
  methods: {
    initTransactions: function() {
      this.transactions = [];
      this.loading = true;
      this.$transAPI
        .getUsersTransactions(this.page, this.numberOfItems, this.type)
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
      let newTrans = new TransactionTableItem(trans, this.exchangeRate);
      this.transactions.push(newTrans);
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
    restorePrevPurchaseDate: function(item) {
      item.date_of_purchase = formatter.getPrettyDate(
        new Date(this.prevPurchaseDate)
      );
    },
    getColor: function(item) {
      return item.profit_percentage > 0 ? "green" : "red";
    },
    changeItemsPerPage: function() {
      if (this.numberOfItems) {
        this.page > 1 ? (this.page = 1) : this.initTransactions();
      }
    }
  },
  watch: {
    exchangeRate: function(newExRate) {
      this.transactions.forEach(trans => {
        if (!trans.isClosedTransaction()) {
          trans.purchase_price = trans.buy_amount / trans.quantity;
          trans.sell_amount = trans.quantity * this.exchangeRate;
          let profit = calcProfit(trans, newExRate);
          trans.profit_usd = profit.profitInUSD;
          trans.profit_percentage = profit.markup;
        }
      });
    },
    newTransaction: function(trans) {
      if (this.type === "open") {
        if (this.numberOfItems > this.transactions.length) {
          this.addNewTransaction(trans);
        } else {
          this.pageCount += 1;
          this.page += 1;
        }
      }
    },
    page: function() {
      this.initTransactions();
    },
    $route(to) {
      this.type = to.fullPath === "/monitor/open" ? "open" : "closed";
      this.page = 1;
      this.initTransactions();
    }
  },
  mounted() {
    this.initTransactions();
  }
};
</script>

<style scoped>
.operations div {
  display: inline-block;
}
</style>
