<template>
    <v-app>
        <TransactionCreator @created="getUsersTransactions"></TransactionCreator>
        <h1>{{exchangeRate}}</h1>
        <TransactionTable
                :items="transactions"
                :exchangeRate="exchangeRate"></TransactionTable>
    </v-app>
</template>

<script>
    import TransactionCreator from "./TransactionCreator";
    import TransactionTable from "./TransactionTable";

    export default {
        name: "CryptoMonitor",
        components: {TransactionTable, TransactionCreator},
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
            setIntervalToExchangeRate: function() {
                this.getExchangeRate()
                setInterval(this.getExchangeRate, 1000)
            },
            getExchangeRate: function () {
                this.$http.get("/api/exchangeRate")
                    .then(response => this.exchangeRate = response.data["exchange_rate"])
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
            this.setIntervalToExchangeRate()
        }
    }
</script>

<style scoped>

</style>