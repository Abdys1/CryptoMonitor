<template>
  <v-app class="content">
    <v-container>
      <v-row>
        <v-col sm="3">
          <TransactionCreator @created="setNewTransaction"></TransactionCreator>
          <br />
          <ExchangeRateIndicator
            @refreshExchangeRate="refreshTable"
          ></ExchangeRateIndicator>
        </v-col>
        <v-col>
          <TransactionTable
            :exchangeRate="exchangeRate"
            :newTransaction="lastTransaction"
          ></TransactionTable>
        </v-col>
      </v-row>
    </v-container>
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

<style scoped>
.content {
  background: url("../assets/login_background.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
}
</style>

<style>
.dg-main-content {
  background-color: #262626;
}

.dg-content {
  color: white;
}

.dg-btn--ok {
  background-color: red;
  border-color: transparent;
  color: white;
}

.dg-btn--ok:active {
  background-color: grey;
}

.dg-btn--cancel {
  color: white;
  background-color: #212121;
}
</style>
