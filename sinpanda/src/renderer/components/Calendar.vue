<template>
  <div>
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title>{{ dtitle }} </v-card-title>
        <v-divider />
        <v-sheet class="px-5 py-10">
          {{ dcontent }}
        </v-sheet>
      </v-card>
    </v-dialog>

    <v-sheet tile height="10vh" color="white" class="d-flex align-center">
      <v-btn outlined small class="ma-4" @click="setToday">
        今日
      </v-btn>
      <v-toolbar-title>{{ title }}</v-toolbar-title>

      <v-btn icon @click="$refs.calendar.prev()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn icon @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-sheet>
    <v-sheet height="90vh">
      <v-calendar
        ref="calendar"
        v-model="value"
        :events="assignments"
        :event-color="getEventColor"
        locale="ja-jp"
        :day-format="timestamp => new Date(timestamp.date).getDate()"
        :month-format="
          timestamp => new Date(timestamp.date).getMonth() + 1 + ' /'
        "
        @click:event="showEvent"
      />
    </v-sheet>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  props: {
    assignments: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  data: () => ({
    events: [],
    value: moment().format('yyyy-MM-DD'),
    dialog: false,
    dtitle: '',
    dcontent: ''
  }),
  computed: {
    title () {
      return moment(this.value).format('yyyy年 M月')
    }
  },
  methods: {
    setToday () {
      this.value = moment().format('yyyy-MM-DD')
    },
    showEvent ({ event }) {
      this.dtitle = event.name
      this.dcontent = event.title + '：締め切り' + event.due
      this.dialog = true
    },
    getEventColor (event) {
      return event.color
    }
  }
}
</script>
