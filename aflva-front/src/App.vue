<template>
  <NavBar/>
  <router-view/>
  <Footer></Footer>
  <div class="toast-container position-fixed top-0 start-50 translate-middle-x p-3">
    <div id="liveToast" class="toast align-items-center text-bg-danger border-0"
         role="alert" aria-live="polite" aria-atomic="true"  data-bs-autohide="true" data-bs-delay="5000">
      <div class="d-flex">
        <div class="toast-body">
          {{ $store.state.error_message }}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
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
