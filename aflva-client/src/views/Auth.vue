<template>
  <div style="margin-top: 80px;">
    <div v-if="update.version" class="alert alert-warning w-75 m-auto" role="alert">
      <h4 class="alert-heading">New version</h4>
      New client version {{ update.version }} available on following link:<span
        class="btn btn-link" @click="browser_url(update.url)">SPAG Client {{ update.version }}</span>.
      <hr>
      <p class="mb-0">After download, just start setup file and it will update everything automatically</p>
    </div>
    <div v-else class='auth-form'>
      <form @submit.prevent="submit()">
        <div class="mb-3">
          <label class="form-label" for="InputEmail">Email address</label>
          <input id="InputEmail" v-model="auth_data.email_or_username" aria-describedby="emailHelp" class="form-control"
                 type="email">
        </div>
        <div class="mb-3">
          <label class="form-label" for="InputPass">Password</label>
          <input id="InputPass" v-model="auth_data.password" class="form-control" type="password">
        </div>
        <div class="error mt-3">
          <div v-show="getUserError" class="alert alert-danger" role="alert">
            {{ getUserError }}
          </div>
        </div>
        <button :disabled="!submit_button" class="btn btn-primary" type="submit">Submit</button>
      </form>
    </div>
    <div class="footer">
      <span>Sky Planet FDR v{{ version }}</span>
    </div>
  </div>

</template>
<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import {version} from "../../package.json";
import axios from "axios";
const { shell } = require('electron')

export default {
  name: 'Auth',
  data() {
    return {
      status: '',
      submit_button: true,
      version: version,
      auth_data: {
        email_or_username: '',
        password: ''
      },
      update: {
        version: null,
        url: null
      }
    }
  },
  computed: {
    getUserError() {
      return this.$store.state.auth_error
    },
  },
  created() {
    this.auth_data.email_or_username = localStorage.email
    this.auth_data.password = localStorage.password
    axios.get('https://api.github.com/repos/nidzhat666/aflva-client/releases/latest')
        .then((res) => {
          let latest = res.data
          if (latest.tag_name !== 'v' + version) {
            this.update = {
              version: latest.tag_name,
              url: latest.assets[0] ? latest.assets[0].browser_download_url : null,
            }
          }
        }).catch(() => {
    });
  },
  methods: {
    submit() {
      this.submit_button = false
      this.$store.dispatch('login', this.auth_data).then(() => {
        this.submit_button = true
        if (this.$store.state.user) {
          this.$router.push({name: 'Book'})
        }
      })
    },
    browser_url(url){
      shell.openExternal(url)
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

  .error {
    max-width: 300px;
    margin: 0 auto;
    transition: opacity 1s ease-out;
  }

  label {
    font-weight: bold;
  }
}
</style>
