<template>
  <v-app>
    <v-main>
      <Calendar :assignments="assignments" />
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'
import moment from 'moment'
import Calendar from '~/components/Calendar.vue'

export default {
  components: {
    Calendar
  },
  data () {
    return {
      response: [],
      assignments: []
    }
  },
  mounted () {
    this.getAssignment()
    setInterval(() => {
      this.getAssignment()
    }, 900000)
  },
  methods: {
    getAssignment () {
      axios
        .get('http://localhost:8000/panda/assignment')
        .then(res => {
          this.response = res.data
          const a = []
          let c = ''
          this.response.forEach(function (elem) {
            const duedate = new Date(elem.fields.assignment).getTime()
            const nowdate = new Date().getTime()
            const limit = (duedate - nowdate) / 1000
            if (limit < 86400) {
              c = 'red'
            } else if (limit < 259200) {
              c = 'orange'
            } else {
              c = 'green'
            }
            a.push({
              name: elem.fields.ltitle,
              start: moment(
                elem.fields.due.substr(0, 4) +
                  '-' +
                  elem.fields.due.substr(5, 2) +
                  '-' +
                  elem.fields.due.substr(8, 2)
              ).toDate(),
              end: moment(
                elem.fields.due.substr(0, 4) +
                  '-' +
                  elem.fields.due.substr(5, 2) +
                  '-' +
                  elem.fields.due.substr(8, 2)
              ).toDate(),
              color: c,
              timed: false,
              due: elem.fields.due,
              title: elem.fields.atitle
            })
          })
          this.assignments = a
        })
        .catch(err => {
          Swal.fire({
            title: 'Error',
            text: "Can't connect to PandA",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000
          })
          return err
        })
    }
  }
}
</script>
