<template>
    <v-data-table
      :headers="headers"
      :items="tableItems"
      class="elevation-1"
    ></v-data-table>
</template>

<script>
    export default {
        name: "TransactionTable",
        props: ["items", "exchangeRate"],
        data: function () {
            return {
                headers: [
                    {text: "Vásárlás dátuma", value: "date_of_purchase"},
                    {text: "Eladás dátuma", value: "date_of_sell"},
                    {text: "Mennyiség", value: "quantity"},
                    {text: "Árfolyam a vásárlás időpontjában", value: "amount"},
                    {text: "Nyereség %", value: "profit_percentage"},
                    {text: "Nyereség $", value: "profit_usd"}
                ]
            }
        },
        computed: {
            tableItems: function() {
                let temp = []
                this.items.forEach(trans => {
                    const profitUSD = this.profitInUSD(trans.quantity, trans.purchase_price)
                    const profitPercentage = this.profitPercentage(trans.quantity, profitUSD)
                    let newTrans = {
                        date_of_purchase: new Date(trans.date_of_purchase).toLocaleString(),
                        date_of_sell: trans.date_of_sell,
                        quantity: trans.quantity,
                        amount: trans.purchase_price,
                        profit_percentage: profitPercentage,
                        profit_usd: profitUSD
                    }
                    temp.push(newTrans)
                })
                return temp
            }
        },
        methods: {
            profitInUSD: function (quantity, purchasePrice) {
                return (quantity * this.exchangeRate) - (quantity * purchasePrice)
            },
            profitPercentage: function (quantity, profitUSD) {
                return (profitUSD / (quantity * this.exchangeRate)) * 100
            }
        }
    }
</script>

<style scoped>

</style>