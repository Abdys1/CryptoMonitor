<template>
  <span>
    <v-icon class="mr-2" small dark @click="openDialog">
      gavel
    </v-icon>
    <CloseDialog
      v-model="dialog"
      :key="componentKey"
      :actual-exchange-rate="exRate"
      @cancel="dialog = false"
      @confirm="closeTransaction"
    >
    </CloseDialog>
  </span>
</template>

<script>
import Transaction from "./util/Transaction";
import CloseDialog from "./dialogs/CloseDialog";

export default {
  name: "TransactionCloseButton",
  components: { CloseDialog },
  props: {
    exchangeRate: Number,
    trans: Object
  },
  data: function() {
    return {
      dialog: false,
      componentKey: 0
    };
  },
  methods: {
    closeTransaction: function(dateOfSell, sellPrice) {
      let newTrans = new Transaction(this.trans);
      newTrans.date_of_sell = dateOfSell;
      newTrans.sell_price = sellPrice;
      this.$transAPI
        .updateTransaction(newTrans)
        .then(() => {
          this.$emit("transClosed", );
          this.dialog = false;
        })
        .catch(response => window.console.log(response));
    },
    openDialog: function() {
      this.componentKey += 1;
      this.dialog = true;
    }
  },
  computed: {
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

<style scoped></style>
