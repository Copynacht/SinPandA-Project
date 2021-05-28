<template>
  <v-app id="app">
    <div>
      <v-tabs fixed-tabs background-color="black" dark>
        <v-tab cols="2" :to="'/'">
          <v-icon medium>mdi-timetable</v-icon>
          時間割
        </v-tab>
        <v-tab cols="4" :to="'assignment'">
          <v-icon medium>mdi-lead-pencil</v-icon>
          課題
        </v-tab>
        <v-tab cols="4" :to="'notification'">
          <v-icon medium>mdi-alert-circle</v-icon>
          お知らせ
        </v-tab>
        <v-tab cols="2" :to="'calendar'">
          <v-icon medium>mdi-calendar-month</v-icon>
          カレンダー
        </v-tab>
      </v-tabs>
      <Nuxt />
    </div>
  </v-app>
</template>

<style>
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

.button--green {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #3b8070;
  color: #3b8070;
  text-decoration: none;
  padding: 10px 30px;
}

.button--green:hover {
  color: #fff;
  background-color: #3b8070;
}

.button--grey {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #35495e;
  color: #35495e;
  text-decoration: none;
  padding: 10px 30px;
  margin-left: 15px;
}

.button--grey:hover {
  color: #fff;
  background-color: #35495e;
}
</style>
