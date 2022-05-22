<template>
  <NavBar/>
  <router-view/>
  <Footer></Footer>
  <div class="toast-container position-fixed top-0 start-0 p-3">
    <div id="liveToast" class="toast border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-body alert alert-danger">
        {{ $store.state.error_message }}
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";

export default {
  components: {NavBar, Footer},
  mounted(){
    this.$store.dispatch('initStorage')
  }
}
</script>
<style lang="scss">

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display:flex;
  flex-direction:column;
  min-height: 100vh;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
