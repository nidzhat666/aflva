<template>
  <div class="header m-5">
    <h4>Sky Planet Aviation Group</h4>
    <h4 v-if="auth">{{auth.first_name}} {{auth.last_name}}</h4>
  </div>
  <div class="footer">
    <span>Sky Planet FDR v2.0</span>
  </div>
</template>

<script>

export default {
  name: "Home",
  data() {
    return {
      auth: false,
    };
  },
};
</script>
<style lang="scss">
.footer{
  position: absolute;
  bottom: 10px;
  width: 100%;
}
.header{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
