<template>
  <div>
    <v-card color="second" class="box">
      <v-card-title>Új tranzakció felvétele</v-card-title>
      <v-card-text>
        <div>
          <v-form ref="form">
            <v-text-field
              label="Elköltött összeg (USDT)"
              prefix="$"
              type="number"
              min="1"
              v-model="buyAmount"
              :rules="validateRules"
            ></v-text-field>
            <v-text-field
              label="Vásárolt mennyiség (BTC)"
              v-model="quantity"
              type="number"
              min="1"
              :rules="validateRules"
            >
            </v-text-field>
            <v-datetime-picker
              label="Vásárlás ideje"
              clear-text="Törlés"
              ok-text="Rendben"
              v-model="purchaseDate"
              :textFieldProps="textFieldProps"
            >
            </v-datetime-picker>
          </v-form>
          <v-btn @click="createNewTransaction">Mentés</v-btn>
        </div>
      </v-card-text>
    </v-card>
    <InfoModal
      :title="infoTitle"
      :message="message"
      v-model="dialog"
      @verify-message="dialog = false"
    ></InfoModal>
  </div>
</template>

<script>
import InfoModal from "../dialogs/InfoModal";

export default {
  name: "TransactionCreator",
  components: { InfoModal },
  data: function() {
    return {
      buyAmount: null,
      quantity: null,
      purchaseDate: null,
      userID: null,
      validateRules: [
        v => !!v || "Kérem adjon meg egy számot!",
        v => parseFloat(v) > 0 || "Kérem adjon meg egy pozitív számot!"
      ],
      textFieldProps: {
        rules: [v => !!v || "Kérem adjon meg egy érvényes dátumot!"]
      },
      dialog: false,
      infoTitle: "",
      message: ""
    };
  },
  methods: {
    createNewTransaction: function() {
      if (this.$refs.form.validate()) {
        const newTrans = this.buildTransaction();
        this.saveTrans(newTrans);
      }
    },
    buildTransaction: function() {
      return {
        quantity: parseFloat(this.quantity),
        buy_amount: parseFloat(this.buyAmount),
        date_of_purchase: this.purchaseDate,
        owner: this.userID
      };
    },
    saveTrans: function(newTrans) {
      this.$transAPI
        .saveTransaction(newTrans)
        .then(createdTrans => {
          this.$refs.form.reset();
          this.showDialog(
            "Új tranzakció",
            "Sikeresen felvetted az új tranzakciót!"
          );
          this.$emit("create", createdTrans);
        })
        .catch(err => {
          this.showDialog(
            "Hiba történt",
            "Nem sikerült véglegesíteni a tranzakciót! Kérlek, próbáld újra!"
          );
          window.console.log(err);
        });
    },
    showDialog(title, msg) {
      this.infoTitle = title;
      this.message = msg;
      this.dialog = true;
    }
  },
  mounted() {
    this.$authAPI
      .getUserInformation()
      .then(info => {
        this.userID = info.id;
      })
      .catch(err => {
        this.showDialog(
          "Hiba történt!",
          "Nem sikerült lekérni a szükséges adatokat!"
        );
        window.console.log(err);
      });
  }
};
</script>

<style scoped></style>
