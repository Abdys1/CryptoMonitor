<template>
    <h1>{{exchangeRate}}</h1>
</template>

<script>
    import Socket from "./socket"

    export default {
        name: "ExchangeRateIndicator",
        data: function() {
            return {
                exchangeRate: 0
            }
        },
        methods: {
            refreshExchangeRate: function (msg) {
                this.exchangeRate = msg
                this.$emit("refreshExchangeRate", this.exchangeRate)
            }
        },
        created(){
			Socket.$on("message", this.refreshExchangeRate)
		},
		beforeDestroy(){
			Socket.$off("message", this.refreshExchangeRate)
		},
        mounted() {
            setInterval(function () {
                Socket.send("get_exchange_rate")
            }, 1300)
        }
    }
</script>

<style scoped>

</style>