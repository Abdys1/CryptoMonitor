<template>
    <v-app>
        <TransactionCreator @created="getUsersTransactions"></TransactionCreator>
        <ExchangeRateIndicator @refreshExchangeRate="refreshTable"></ExchangeRateIndicator>
        <TransactionTable
                :items="transactions"
                :exchangeRate="exchangeRate"></TransactionTable>
    </v-app>
</template>

<script>
    import TransactionCreator from "./TransactionCreator";
    import TransactionTable from "./TransactionTable";
    import ExchangeRateIndicator from "./ExchangeRateIndicator";

    export default {
        name: "CryptoMonitor",
        components: {ExchangeRateIndicator, TransactionTable, TransactionCreator},
        data: function() {
            return {
                transactions: [],
                exchangeRate: 0
            }
        },
        methods: {
            getUsersTransactions: function() {
                this.$http.get("/api/transaction/")
                    .then(response => this.transactions = response.data)
            },
            refreshTable: function (exRate) {
                this.exchangeRate = exRate
            }
        },
        beforeCreate() {
            if(this.$session.exists()) {
                this.$http.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem("token")
            }
            else {
                this.$http.defaults.headers.common["Authorization"] = ""
                localStorage.removeItem("token")
                this.$router.push("/")
            }
        },
        mounted() {
            this.getUsersTransactions()
        }
    }
</script>

<style scoped>

</style>