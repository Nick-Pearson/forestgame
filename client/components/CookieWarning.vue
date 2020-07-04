<template>
  <div class="cookie-warning" v-if="showWarning">
    <span>
      Cookies are required to play this game <button class="inline-button" v-on:click="ok">OK</button> <button class="inline-button" v-on:click="moreinfo">More information</button>
    </span>
  </div>
</template>

<style>
.cookie-warning
{
  margin: -20px -20px 10px -20px;
  padding: 5px;
  background-color: #0666A4;
  color: #EEEEEE;
  text-shadow: 1px 1px #000000;
  box-shadow: 0 1px 5px 0px #000000;
}
</style>

<script>
function setCookie(cname, cvalue, exdays) 
{
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) 
{
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) 
  {
    var c = ca[i];
    while (c.charAt(0) == ' ') 
    {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0)
    {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const model = {
  showWarning: false
};

export default {
  name: 'CookieWarning',
  data: () => model,
  methods: {
    ok: function() {
      setCookie("forestgame_cookies_accepted", true);
      model.showWarning = false;
    },
    moreinfo: function() {
      this.$router.push({name: "cookies"});
    }
  },
  mounted: function() {
    const accepted = getCookie("forestgame_cookies_accepted");
    model.showWarning = (accepted !== "true");
  },
}
</script>