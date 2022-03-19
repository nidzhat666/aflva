<template>
  <div class="header">
    <div class="container d-flex flex-column flex-md-row align-items-center p-3 ">
      <a href="/" class="d-flex align-items-center text-dark text-decoration-none">
        <img class="logo" src="../assets/img/aflva_logo.png" alt="">
      </a>

      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
        <a class="me-3 py-2 text-dark text-decoration-none text-white" href="#" v-for="tab in tabs"
           :key="tab.id">{{ tab.text }}</a>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      tabs: [
        {'text': 'Schedules'},
        {'text': 'Fleet'},
        {'text': 'Crew'},
        {'text': 'Online'},
        {'text': 'Route'},
        {'text': 'Admin'},
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  background-color: #02458d;

  .logo {
    max-width: 210px;
  }
}

</style>
