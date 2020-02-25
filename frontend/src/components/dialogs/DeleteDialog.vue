<template>
  <v-row justify="center">
    <v-dialog v-model="show" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Tranzakció törlése</v-card-title>
        <v-card-text>Biztosan törölni szeretnéd a tranzakciót?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="close()">Mégsem</v-btn>
          <v-btn color="green darken-1" text @click="confirm()">Törlés</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "DeleteDialog",
  props: {
    value: Boolean,
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
      this.$emit("confirm");
    }
  }
};
</script>

<style scoped></style>
