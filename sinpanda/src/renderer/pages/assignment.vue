<template>
  <v-container>
    <div v-for="(a, key) in aa" :key="key" class="cont">
      <ul @click="jump(key)">
        <li
          v-if="a.fields.assignment < 86400 && a.fields.assignment !== 0"
          class="redli"
        >
          <font size="5">
            <b>
              ＜締め切りまで残り<font size="5" color="red">{{
                a.fields.limit
              }}</font>です＞</b>
          </font><v-divider />
          <font size="4">
            講義名：{{ a.fields.ltitle }}<br>
            課題名：{{ a.fields.atitle }}<br>
            締切り：{{ a.fields.due }}<br>
            提出受付期限：{{ a.fields.drop }}<br>
          </font>
        </li>
        <li
          v-else-if="a.fields.assignment < 259200 && a.fields.assignment !== 0"
          class="orangeli"
        >
          <font size="5">
            <b>
              ＜締め切りまで残り<font size="5" color="red">{{
                a.fields.limit
              }}</font>です＞</b>
          </font><v-divider />
          <font size="4">
            講義名：{{ a.fields.ltitle }}<br>
            課題名：{{ a.fields.atitle }}<br>
            締切り：{{ a.fields.due }}<br>
            提出受付期限：{{ a.fields.drop }}<br>
          </font>
        </li>
        <li v-else-if="a.fields.assignment !== 0" class="greenli">
          <font size="5">
            <b>
              ＜締め切りまで残り<font size="5" color="red">{{
                a.fields.limit
              }}</font>です＞</b>
          </font><v-divider />
          <font size="4">
            講義名：{{ a.fields.ltitle }}<br>
            課題名：{{ a.fields.atitle }}<br>
            締切り：{{ a.fields.due }}<br>
            提出受付期限：{{ a.fields.drop }}<br>
          </font>
        </li>
      </ul>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  data () {
    return {
      aa: []
    }
  },
  mounted () {
    this.getAssignment()
    setInterval(() => {
      this.getAssignment()
    }, 60000)
  },
  methods: {
    jump (key) {
      const jumpURL = this.aa[key].fields.url
      const { shell } = require('electron')
      shell.openExternal(jumpURL)
    },
    getAssignment () {
      axios
        .get('http://localhost:8000/panda/assignment')
        .then(res => {
          this.aa = res.data
          let once = true
          for (let x = 0; x < this.aa.length; x++) {
            const duedate = new Date(this.aa[x].fields.assignment).getTime()
            const nowdate = new Date().getTime()
            let duelimit = (duedate - nowdate) / 1000
            if (duelimit < 0) {
              duelimit = 0
              if (once === true) {
                axios
                  .get('http://localhost:8000/panda/timetableupdate')
                  .catch(err => {
                    return err
                  })
                axios
                  .get('http://localhost:8000/panda/assignmentupdate')
                  .catch(err => {
                    return err
                  })
                once = false
              }
            }
            this.aa[x].fields.assignment = duelimit
            this.aa[x].fields.limit =
              Math.floor(duelimit / 86400) +
              '日' +
              Math.floor((duelimit % 86400) / 3600) +
              '時間' +
              Math.floor((duelimit % 3600) / 60) +
              '分'
          }
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

<style scoped>
.cont ul {
  padding: 0;
  position: relative;
}

.cont .greenli {
  color: black;
  border-left: solid 8px limegreen; /*左側の線*/
  background: whitesmoke; /*背景色*/
  margin-bottom: 5px; /*下のバーとの余白*/
  line-height: 1.5;
  border-radius: 0 15px 15px 0; /*右側の角だけ丸く*/
  padding: 0.5em;
  list-style-type: none !important;
}

.cont .orangeli {
  color: black;
  border-left: solid 8px orange; /*左側の線*/
  background: whitesmoke; /*背景色*/
  margin-bottom: 5px; /*下のバーとの余白*/
  line-height: 1.5;
  border-radius: 0 15px 15px 0; /*右側の角だけ丸く*/
  padding: 0.5em;
  list-style-type: none !important;
}

.cont .redli {
  color: black;
  border-left: solid 8px red; /*左側の線*/
  background: whitesmoke; /*背景色*/
  margin-bottom: 5px; /*下のバーとの余白*/
  line-height: 1.5;
  border-radius: 0 15px 15px 0; /*右側の角だけ丸く*/
  padding: 0.5em;
  list-style-type: none !important;
}
</style>
