<template>
  <v-container>
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title>メニュー</v-card-title>
        <v-divider />
        <v-sheet class="px-5 py-10">
          <v-row cols="12">
            <v-col v-for="(icon, keyicon) in menuIcon" :key="keyicon" cols="3">
              <v-row justify="center" align-content="center">
                <v-icon x-large @click="jump(icon.url)">{{ icon.mdi }}</v-icon>
              </v-row>
            </v-col>
            <v-col
              v-for="(icon, keyicon) in menuIcon"
              :key="'i' + keyicon"
              cols="3"
            >
              <v-row justify="center" align-content="center">
                {{ icon.jap }}
              </v-row>
            </v-col>
          </v-row>
        </v-sheet>
      </v-card>
    </v-dialog>
    <table v-if="!loading">
      <tr>
        <th>
          <v-icon x-large color="white" @click="panda()">mdi-panda</v-icon>
        </th>
        <th>月曜</th>
        <th>火曜</th>
        <th>水曜</th>
        <th>木曜</th>
        <th>金曜</th>
      </tr>
      <tr v-for="(tr, key1) in timetable" :key="key1">
        <th>{{ tLabel[key1] }}</th>
        <td
          v-if="tr[0].assignment < 86400 && tr[0].assignment !== 0"
          class="redtd"
          @click="openDialog(key1, 0)"
        >
          <div>
            {{ tr[0].title }}
          </div>
        </td>
        <td
          v-else-if="tr[0].assignment < 259200 && tr[0].assignment !== 0"
          class="orangetd"
          @click="openDialog(key1, 0)"
        >
          <div>
            {{ tr[0].title }}
          </div>
        </td>
        <td
          v-else-if="tr[0].assignment !== 0 && tr[0].assignment !== null"
          class="greentd"
          @click="openDialog(key1, 0)"
        >
          <div>
            {{ tr[0].title }}
          </div>
        </td>
        <td v-else class="normaltd" @click="openDialog(key1, 0)">
          <div>
            {{ tr[0].title }}
          </div>
        </td>
        <td
          v-if="tr[1].assignment < 86400 && tr[1].assignment !== 0"
          class="redtd"
          @click="openDialog(key1, 1)"
        >
          <div>
            {{ tr[1].title }}
          </div>
        </td>
        <td
          v-else-if="tr[1].assignment < 259200 && tr[1].assignment !== 0"
          class="orangetd"
          @click="openDialog(key1, 1)"
        >
          <div>
            {{ tr[1].title }}
          </div>
        </td>
        <td
          v-else-if="tr[1].assignment !== 0 && tr[1].assignment !== null"
          class="greentd"
          @click="openDialog(key1, 1)"
        >
          <div>
            {{ tr[1].title }}
          </div>
        </td>
        <td v-else class="normaltd" @click="openDialog(key1, 1)">
          <div>
            {{ tr[1].title }}
          </div>
        </td>
        <td
          v-if="tr[2].assignment < 86400 && tr[2].assignment !== 0"
          class="redtd"
          @click="openDialog(key1, 2)"
        >
          <div>
            {{ tr[2].title }}
          </div>
        </td>
        <td
          v-else-if="tr[2].assignment < 259200 && tr[2].assignment !== 0"
          class="orangetd"
          @click="openDialog(key1, 2)"
        >
          <div>
            {{ tr[2].title }}
          </div>
        </td>
        <td
          v-else-if="tr[2].assignment !== 0"
          class="greentd"
          @click="openDialog(key1, 2)"
        >
          <div>
            {{ tr[2].title }}
          </div>
        </td>
        <td v-else class="normaltd" @click="openDialog(key1, 2)">
          <div>
            {{ tr[2].title }}
          </div>
        </td>
        <td
          v-if="tr[3].assignment < 86400 && tr[3].assignment !== 0"
          class="redtd"
          @click="openDialog(key1, 3)"
        >
          <div>
            {{ tr[3].title }}
          </div>
        </td>
        <td
          v-else-if="tr[3].assignment < 259200 && tr[3].assignment !== 0"
          class="orangetd"
          @click="openDialog(key1, 3)"
        >
          <div>
            {{ tr[3].title }}
          </div>
        </td>
        <td
          v-else-if="tr[3].assignment !== 0"
          class="greentd"
          @click="openDialog(key1, 3)"
        >
          <div>
            {{ tr[3].title }}
          </div>
        </td>
        <td v-else class="normaltd" @click="openDialog(key1, 3)">
          <div>
            {{ tr[3].title }}
          </div>
        </td>
        <td
          v-if="tr[4].assignment < 86400 && tr[4].assignment !== 0"
          class="redtd"
          @click="openDialog(key1, 4)"
        >
          <div>
            {{ tr[4].title }}
          </div>
        </td>
        <td
          v-else-if="tr[4].assignment < 259200 && tr[4].assignment !== 0"
          class="orangetd"
          @click="openDialog(key1, 4)"
        >
          <div>
            {{ tr[4].title }}
          </div>
        </td>
        <td
          v-else-if="tr[4].assignment !== 0 && tr[4].assignment !== null"
          class="greentd"
          @click="openDialog(key1, 4)"
        >
          <div>
            {{ tr[4].title }}
          </div>
        </td>
        <td v-else class="normaltd" @click="openDialog(key1, 4)">
          <div>
            {{ tr[4].title }}
          </div>
        </td>
      </tr>
    </table>
  </v-container>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      tt: [],
      timetable: [],
      menuIcon: [
        { jap: "お知らせ", mdi: "mdi-alert-circle", url: "notiURL" },
        { jap: "講義資料", mdi: "mdi-note-multiple", url: "resoURL" },
        { jap: "課題", mdi: "mdi-lead-pencil", url: "assiURL" },
        { jap: "Zoom", mdi: "mdi-desktop-mac", url: "zoomURL" }
      ],
      tLabel: ["1限", "2限", "3限", "4限", "5限"],
      menuId: 0,
      loading: false,
      dialog: false,
    };
  },
  mounted() {
    this.getTimeTable();
    setInterval(() => {
      this.getTimeTable();
    }, 900000);
  },
  methods: {
    openDialog(key1, key2) {
      if (this.tt[key1 * 5 + key2].fields.title !== null) {
        this.menuId = key1 * 5 + key2;
        this.dialog = true;
      }
    },
    jump(url) {
      const jumpURL = this.tt[this.menuId].fields[url];
      const { shell } = require("electron");
      shell.openExternal(jumpURL);
    },
    panda() {
      const { shell } = require("electron");
      shell.openExternal("https://panda.ecs.kyoto-u.ac.jp/portal/");
    },
    getTimeTable() {
      this.loading = true;
      axios
        .get("http://localhost:8000/panda/timetable")
        .then(res => {
          this.tt = res.data;
          if (this.tt.length === 0) {
            throw new Error("No Data");
          }
          for (let x = 0; x < 5; x++) {
            this.timetable[x] = [];
            for (let y = 0; y < 5; y++) {
              this.timetable[x].push(this.tt[x * 5 + y].fields);
              if (
                this.timetable[x][y].assignment !== null &&
                this.timetable[x][y].assignment !== ""
              ) {
                const duedate = new Date(
                  this.timetable[x][y].assignment
                ).getTime();
                const nowdate = new Date().getTime();
                this.timetable[x][y].assignment = (duedate - nowdate) / 1000;
              } else {
                this.timetable[x][y].assignment = 0;
              }
            }
          }
          this.loading = false;
        })
        .catch(err => {
          if (err === "No Data") {
            Swal.fire({
              title: "Error",
              text: "No Data Responded",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000
            });
          } else {
            Swal.fire({
              title: "Error",
              text: "Can't connect to PandA",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000
            });
          }
          this.loading = false;
          return err;
        });
    }
  }
};
</script>

<style scoped>
table {
  border-collapse: separate;
  border-spacing: 3px;
  width: 100%;
  table-layout: fixed;
}

table th,
table td {
  border-radius: 3px;
  text-align: center;
  padding: 10px 0;
}

table th {
  font-size: x-large;
  background-color: black;
  color: white;
}

table td {
  border: solid 1px black;
}

table .normaltd {
  font-weight: bold;
  background-color: white;
}

table .greentd {
  font-weight: bold;
  background-color: limegreen;
}

table .orangetd {
  font-weight: bold;
  background-color: orange;
}

table .redtd {
  font-weight: bold;
  background-color: red;
}
</style>
