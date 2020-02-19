<template>
  <v-row justify="center">
    <v-dialog v-model="show" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Tranzakció lezárása</v-card-title>
        <v-form ref="closeForm">
          <v-text-field
            label="Árfolyam az értékesítés pillanatában"
            prefix="$"
            type="number"
            v-model="sellPrice"
            :rules="rules"
          ></v-text-field>
          <v-datetime-picker v-model="sellDate" label="Értékesítés dátuma">
            <template slot="actions" slot-scope="{ parent }">
              <v-btn color="success darken-1" @click="parent.okHandler()"
                >Rendben</v-btn
              >
            </template>
          </v-datetime-picker>
        </v-form>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="close">Mégsem</v-btn>
          <v-btn color="green darken-1" text @click="confirm">Lezárás</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "CloseDialog",
  props: {
    value: Boolean,
    actualExchangeRate: Number
  },
  data: function() {
    return {
      sellPrice: this.actualExchangeRate,
      sellDate: new Date(),
      rules: [v => !!v || "Kérem adjon meg egy érvényes értéket!"]
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      }
    }
  },
  methods: {
    close: function() {
      this.$emit("cancel");
    },
    confirm: function() {
      if (this.$refs.closeForm.validate()) {
        this.$emit("confirm", this.sellDate, this.sellPrice);
      }
    }
  }
};
</script>

<style scoped></style>
