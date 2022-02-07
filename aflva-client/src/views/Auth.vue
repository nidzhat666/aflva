<template>
  <div class='auth-form' style="margin-top: 80px;">
    <form @submit.prevent="submit()">
      <div class="mb-3">
        <label for="InputEmail" class="form-label">Email address</label>
        <input v-model="auth_data.email_or_username" type="email" class="form-control" id="InputEmail"
               aria-describedby="emailHelp">
      </div>
      <div class="mb-3">
        <label for="InputPass" class="form-label">Password</label>
        <input v-model="auth_data.password" type="password" class="form-control" id="InputPass">
      </div>
      <div class="error mt-3">
        <div v-show="getUserError" class="alert alert-danger" role="alert">
          {{ getUserError }}
        </div>
      </div>
      <button type="submit" class="btn btn-primary" :disabled="!submit_button">Submit</button>
    </form>
    <div class="footer">
      <span>Sky Planet FDR v2.0</span>
    </div>
  </div>
</template>
<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import keytar from 'keytar'

export default {
  name: 'Auth',
  data() {
    return {
      status: '',
      submit_button: true,
      auth_data: {
        email_or_username: '',
        password: ''
      }
    }
  },
  computed: {
    getUserError() {
      return this.$store.state.auth_error
    },
  },
  created(){
    keytar.findCredentials('afl').then(data=>{
      if (data.length){
        this.auth_data.email_or_username = data[0].account
        this.auth_data.password = data[0].password
      }
    })
  },
  methods: {
    submit() {
      this.submit_button = false
      this.$store.dispatch('login', this.auth_data).then(()=>{
        this.submit_button = true
        if(this.$store.state.user){
          this.$router.push({name:'Book'})
        }
      })
    }
  }
}
</script>
<style lang="scss">
.auth-form {
  form {
    max-width: 200px;
    margin: 0 auto;
  }
  .error{
    max-width: 300px;
    margin: 0 auto;
    transition: opacity 1s ease-out;
  }
}
</style>
