<template>
  <div>
    <v-card color="second">
      <v-card-title>Új tranzakció felvétele</v-card-title>
      <v-card-text>
        <div>
          <v-form ref="form">
            <v-text-field
              label="Árfolyam"
              prefix="$"
              type="number"
              v-model="amount"
              :rules="validateRules"
            ></v-text-field>
            <v-text-field
              label="Mennyiség"
              v-model="quantity"
              type="number"
              :rules="validateRules"
            >
            </v-text-field>
            <v-menu
              v-model="menu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="date"
                  label="Vásárlás dátuma"
                  prepend-icon="event"
                  readonly
                  v-on="on"
                  :rules="validateRules"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="date"
                @input="menu = false"
              ></v-date-picker>
            </v-menu>
            <v-menu
              ref="menu"
              v-model="menu2"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="time"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time"
                  label="Vásárlás ideje"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                  :rules="validateRules"
                ></v-text-field>
              </template>
              <v-time-picker
                v-if="menu2"
                v-model="time"
                full-width
                @click:minute="$refs.menu.save(time)"
              ></v-time-picker>
            </v-menu>
          </v-form>
          <v-btn @click="createNewTransaction">Mentés</v-btn>
        </div>
      </v-card-text>
    </v-card>
    <InfoModal
      title="Új tranzakció"
      message="Sikeresen felvetted az új tranzakciót!"
      v-model="dialog"
      @verify-message="dialog = false"
    ></InfoModal>
  </div>
</template>

<script>
import InfoModal from "./InfoModal";
export default {
  name: "TransactionCreator",
  components: { InfoModal },
  data: function() {
    return {
      amount: null,
      quantity: null,
      date: null,
      time: null,
      menu: false,
      menu2: false,
      userID: null,
      validateRules: [v => !!v || "Kérem adjon meg egy érvényes értéket!"],
      dialog: false
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
      const dateString = this.date + " " + this.time;
      const purchaseDate = new Date(dateString);
      return {
        quantity: parseFloat(this.quantity),
        purchase_price: parseFloat(this.amount),
        date_of_purchase: purchaseDate,
        owner: this.userID
      };
    },
    saveTrans: function(newTrans) {
      this.$transAPI
        .saveTransaction(newTrans)
        .then(createdTrans => {
          this.$refs.form.reset();
          this.dialog = true;
          this.$emit("created", createdTrans);
        })
        .catch(err => window.console.log(err));
    }
  },
  beforeCreate() {
    this.$http
      .get("/auth/account")
      .then(response => (this.userID = response.data.id))
      .catch(err => window.console.log(err));
  }
};
</script>

<style scoped></style>
