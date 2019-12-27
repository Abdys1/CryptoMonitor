import Vue from 'vue';
import Vuetify from 'vuetify/lib';

import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
          dark: {
              primary: colors.yellow.darken1,
              second: colors.yellow.darken1,
              accent: colors.yellow.darken1,
              error: colors.red.accent3,
              anchor: colors.yellow.darken1,
              info: colors.yellow.darken1,
              success: colors.yellow.darken1,
              warning: '#ffbb33'
          },
        },
    },
});
