<template>
  <div>
    <h1>{{ parseFloat(sumProfit).toFixed(2) }}</h1>
  </div>
</template>

<script>
export default {
  name: "TransactionStatistics",
  data: function() {
    return {
      sumProfit: 0,
      sumBTC: 0,
      closedTransactionProfit: 0,
      averageProfit: 0
    };
  },
  methods: {
    calcStatistics: function() {
      this.transactions.forEach(trans => {
        this.sumProfit += trans.profit_usd;
      });
    }
  },
  mounted() {
    this.calcStatistics();
  }
};
</script>

<style scoped></style>
