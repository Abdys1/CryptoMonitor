<template>
  <v-card color="second">
    <v-card-title>Aktuális árfolyam</v-card-title>
    <v-card-text>
      <div>
        <h1>{{ exchangeRate }}</h1>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from "vue";

export default {
  name: "ExchangeRateIndicator",
  data: function() {
    return {
      exchangeRate: 0
    };
  },
  mounted() {
    this.$connect();
    setInterval(function() {
      if (Vue.prototype.$socket.readyState === 1) {
        Vue.prototype.$socket.send("get_exchange_rate");
      }
    }, 1500);
    this.$options.sockets.onmessage = function(msg) {
      this.exchangeRate = parseFloat(parseFloat(msg.data).toFixed(2));
      this.$emit("refreshExchangeRate", this.exchangeRate);
    };
  }
};
</script>

<style scoped></style>
