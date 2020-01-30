<template>
  <v-app>
    <TransactionCreator @created="setNewTransaction"></TransactionCreator>
    <ExchangeRateIndicator
      @refreshExchangeRate="refreshTable"
    ></ExchangeRateIndicator>
    <TransactionTable
      :exchangeRate="exchangeRate"
      :newTransaction="lastTransaction"
    ></TransactionTable>
  </v-app>
</template>

<script>
import TransactionCreator from "./TransactionCreator";
import TransactionTable from "./TransactionTable";
import ExchangeRateIndicator from "./ExchangeRateIndicator";

export default {
  name: "CryptoMonitor",
  components: { ExchangeRateIndicator, TransactionTable, TransactionCreator },
  data: function() {
    return {
      exchangeRate: 0,
      lastTransaction: null
    };
  },
  methods: {
    refreshTable: function(exRate) {
      this.exchangeRate = exRate;
    },
    setNewTransaction: function(newTrans) {
      this.lastTransaction = newTrans;
    }
  },
  beforeCreate() {
    if (this.$session.exists()) {
      this.$http.defaults.headers.common["Authorization"] =
        "Token " + localStorage.getItem("token");
    } else {
      this.$http.defaults.headers.common["Authorization"] = "";
      window.cookie = "Authorization=";
      localStorage.removeItem("token");
      this.$router.push("/");
    }
  }
};
</script>

<style scoped></style>
