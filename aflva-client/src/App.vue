<template>
  <div class="header m-3">
    <h4>Sky Planet Aviation Group</h4>
    <h4 v-if="getAuth">{{ getAuth.first_name }} {{getAuth.last_name}}</h4>
  </div>
  <div class="content">
    <Auth v-if="!getAuth"/>
    <Book v-else/>
  </div>
</template>
<script>
import Auth from "@/views/Auth";
import Book from "@/views/Book";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
export default {
  data(){
  },
  components:{
    Auth,
    Book
  },
  computed: {
    getAuth() {
      return this.$store.state.user
    },
    getBook() {
      return this.$store.state.books
    }
  },
  mounted(){
    if (this.getAuth){
      this.$router.push({'name':'Book'})
    }else{
      this.$router.push({'name':'Login'})
    }
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
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}

.footer {
  position: absolute;
  bottom: 10px;
  width: 100%;
  text-align: center;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
