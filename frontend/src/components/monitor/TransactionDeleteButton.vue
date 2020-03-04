<template>
  <div>
    <v-icon small dark @click="dialog = true">
      delete
    </v-icon>
    <DeleteDialog
      v-model="dialog"
      @cancel="dialog = false"
      @confirm="deleteTransaction"
    ></DeleteDialog>
  </div>
</template>

<script>

import DeleteDialog from "../dialogs/DeleteDialog";
export default {
  name: "TransactionDeleteButton",
  components: {DeleteDialog},
  props: { transId: Number },
  data: function() {
    return {
      dialog: false
    };
  },
  methods: {
    deleteTransaction: function() {
      this.$transAPI
        .deleteTransaction(this.transId)
        .then(() => {
          this.dialog = false;
          this.$emit("transDeleted");
        })
        .catch(() => {
          window.console.log("Hiba");
        });
    }
  }
};
</script>

<style scoped></style>
