<template>
  <v-row justify="center">
    <v-dialog v-model="show" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Tranzakció lezárása</v-card-title>
        <v-form>
          <v-text-field
            label="Árfolyam az értékesítés pillanatában"
            prefix="$"
            type="number"
            v-model="sellPrice"
          ></v-text-field>
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
                label="Értékesítés napja"
                prepend-icon="event"
                readonly
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="date" @input="menu = false"></v-date-picker>
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
                label="Értékesítés ideje"
                prepend-icon="access_time"
                readonly
                v-on="on"
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
    value: Boolean
  },
  data: function() {
    return {
      menu: false,
      date: null,
      menu2: false,
      time: null,
      sellPrice: null
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
        const dateString = this.date + " " + this.time;
        const dateOfSell = new Date(dateString);
        this.$emit("confirm", dateOfSell, this.sellPrice);
    }
  }
};
</script>

<style scoped></style>
