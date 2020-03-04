<template>
  <v-card color="second" class="box">
    <v-card-title>Valutaváltó</v-card-title>
    <v-card-text>
      <v-select :items="items" menu-props="auto" v-model="selected"></v-select>
      <div v-if="selected === 'USDT -> BTC'">
        <v-text-field label="USD" v-model="usd"></v-text-field>
        <h2>{{ parseFloat(calculatedBTC).toFixed(4) + ' BTC' }}</h2>
      </div>
      <div v-if="selected === 'BTC -> USDT'">
        <v-text-field label="BTC" v-model="btc"></v-text-field>
        <h2>{{ parseFloat(calculatedUSD).toFixed(2) + ' USDT' }}</h2>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "CurrencyExchangePoint",
  props: {
    exchangeRate: Number
  },
  data: function() {
    return {
      usd: 0,
      btc: 0,
      items: ['USDT -> BTC', 'BTC -> USDT'],
      selected: 'USDT -> BTC'
    };
  },
  computed: {
    calculatedBTC: function() {
      return this.usd / this.exRate;
    },
    calculatedUSD: function() {
      return this.btc * this.exRate;
    },
    exRate: {
      get() {
        return this.exchangeRate;
      },
      set(value) {
        this.$emit("input", value);
      }
    }
  }
};
</script>

<style scoped>
</style>
