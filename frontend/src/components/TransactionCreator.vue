<template>
    <v-form ref="form">
        <v-text-field
            label="Aktuális érték a vásárlás időpontjában"
            prefix="$"
            type="number"
            v-model="amount"
        ></v-text-field>
        <v-text-field
            label="Bitcoin mennyiség"
            v-model="quantity"
            type="number"
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
              label="Picker without buttons"
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
              label="Picker in menu"
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
</template>

<script>
    export default {
        name: "TransactionCreator",
        data: function () {
            return {
                amount: null,
                quantity: null,
                date: null,
                time: null,
                menu: false,
                menu2: false
            }
        }
    }
</script>

<style scoped>

</style>