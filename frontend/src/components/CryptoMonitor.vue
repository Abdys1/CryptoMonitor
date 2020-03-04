<template>
  <v-app class="content">
    <v-app-bar app dark>
      <v-toolbar-title>Kriptomonitor</v-toolbar-title>
      <v-spacer />
      <v-btn class="mx-2" fab dark @click="exitApp">
        <v-icon>mdi-exit-to-app</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content>
      <v-container>
        <v-row>
          <v-col>
            <TransactionCreator
              @create="setNewTransaction"
            ></TransactionCreator>
            <br />
            <ExchangeRateIndicator
              @refreshExchangeRate="refreshExRate"
            ></ExchangeRateIndicator>
            <br/>
            <CurrencyExchangePoint
              :exchange-rate="exchangeRate">
            </CurrencyExchangePoint>
          </v-col>
          <v-col lg="10">
            <TransactionTable
              :exchangeRate="exchangeRate"
              :newTransaction="newTransaction"
            ></TransactionTable>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import TransactionCreator from "./monitor/TransactionCreator";
import TransactionTable from "./monitor/TransactionTable";
import ExchangeRateIndicator from "./monitor/ExchangeRateIndicator";
import CurrencyExchangePoint from "./monitor/CurrencyExchangePoint";

export default {
  name: "CryptoMonitor",
  components: {CurrencyExchangePoint, ExchangeRateIndicator, TransactionTable, TransactionCreator },
  data: function() {
    return {
      exchangeRate: 0,
      newTransaction: null
    };
  },
  methods: {
    refreshExRate: function(exRate) {
      this.exchangeRate = exRate;
    },
    setNewTransaction: function(newTrans) {
      this.newTransaction = newTrans;
    },
    exitApp: function () {
      this.$http.defaults.headers.common["Authorization"] = "";
      window.cookie = "Authorization=";
      this.$session.destroy();
      this.$router.push("/");
    }
  },
  beforeCreate() {
    if (this.$session.exists()) {
      this.$http.defaults.headers.common["Authorization"] =
        "Token " + this.$session.get("jwt");
    } else {
      this.exitApp();
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
