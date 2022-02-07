<template>
  <div id="myModal" data-bs-backdrop="static" class="modal fade">
    <div class="modal-dialog modal-confirm modal-sm ">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" style="color: white">Error</h5>
        </div>
        <div class="modal-body text-center">
          <p class="mt-3">{{ message }}</p>
          <button class="btn btn-success" v-on:click="$emit('message', false)" data-bs-dismiss="modal">Ok</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js";

export default {
  name: "ErrorModal",
  props: ['message'],
  data() {
    return {
      modal: null,
    }
  },
  watch: {
    message(newMessage, oldMessage) {
      console.log(newMessage, oldMessage)
      this.modal.show()
    }
  },
  mounted() {
    this.modal = new bootstrap.Modal(document.getElementById('myModal'), {})
  },
  methods: {}
}
</script>

<style scoped>
.modal-body{
  padding: 0;
}
.modal-confirm {
  color: #434e65;
  width: 525px;
  margin: 30px auto;
}
.modal-confirm .modal-content {
  padding: 20px;
  font-size: 16px;
  border-radius: 5px;
  border: none;
}
.modal-confirm .modal-header {
  background: #e85e6c;
  border-bottom: none;
  position: relative;
  text-align: center;
  margin: -20px -20px 0;
  border-radius: 5px 5px 0 0;
}
.modal-confirm h4 {
  text-align: center;
  font-size: 36px;
  margin: 10px 0;
}
.modal-confirm .form-control, .modal-confirm .btn {
  min-height: 40px;
  border-radius: 3px;
}
.modal-confirm .close {
  position: absolute;
  top: 15px;
  right: 15px;
  color: #fff;
  text-shadow: none;
  opacity: 0.5;
}
.modal-confirm .close:hover {
  opacity: 0.8;
}
.modal-confirm .icon-box {
  color: #fff;
  width: 95px;
  height: 95px;
  display: inline-block;
  border-radius: 50%;
  z-index: 9;
  border: 5px solid #fff;
  padding: 15px;
  text-align: center;
}
.modal-confirm .icon-box i {
  font-size: 58px;
  margin: -2px 0 0 -2px;
}
.modal-confirm.modal-dialog {
  margin-top: 80px;
}
.modal-confirm .btn {
  color: #fff;
  border-radius: 4px;
  background: #eeb711;
  text-decoration: none;
  transition: all 0.4s;
  line-height: normal;
  margin-top: 10px;
  padding: 6px 20px;
  min-width: 150px;
  border: none;
}
.modal-confirm .btn:hover, .modal-confirm .btn:focus {
  background: #eda645;
  outline: none;
}
.trigger-btn {
  display: inline-block;
  margin: 100px auto;
}
</style>
