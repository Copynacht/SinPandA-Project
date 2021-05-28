<template>
  <v-container>
    <div v-for="(n, key) in nn" :key="key" class="cont">
      <ul @click="jump(key)">
        <li>
          <font size="5">
            <b>{{ n.fields.ann }}</b>
          </font><br>
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
      nn: []
    }
  },
  mounted () {
    this.getNotification()
    setInterval(() => {
      this.getNotification()
    }, 900000)
  },
  methods: {
    jump (key) {
      const jumpURL = this.nn[key].fields.url
      const { shell } = require('electron')
      shell.openExternal(jumpURL)
    },
    getNotification () {
      axios
        .get('http://localhost:8000/panda/announce')
        .then(res => {
          this.nn = res.data
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
.cont ul,
ol {
  padding: 0;
  position: relative;
}

.cont ul li,
ol li {
  color: black;
  border-left: solid 8px black; /*左側の線*/
  background: whitesmoke; /*背景色*/
  margin-bottom: 5px; /*下のバーとの余白*/
  line-height: 1.5;
  border-radius: 0 15px 15px 0; /*右側の角だけ丸く*/
  padding: 0.5em;
  list-style-type: none !important;
}
</style>
