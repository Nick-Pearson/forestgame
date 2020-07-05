<template>
  <div class="event-feed">
    <div class="event-msg" v-for="item in messages"  :key="item.id">
      <p><span class="time">{{formatTime(item.time)}}</span> {{item.text}}</p>
    </div>
  </div>
</template>

<style scoped>
.event-feed
{
  z-index: 300;
  position: absolute;
  bottom: 0;
  right: 0;
  width: 250px;
}

.event-msg
{
  background-color: #333333;
  color: #ffffff;
  margin: 0;
  padding: 4px 10px 4px 10px;
}

.event-msg:nth-child(2)
{
  background-color: #3F3F3F;
}

.event-msg p
{
  margin: 0;
  user-select: none;
}

.time
{
  color: #888888;
}
</style>

<script>
let model = {
  messages: []
}

export default {
  data: () => model,
  methods: {
    "formatTime": function(time) {
      return `[${time.getHours().toString().padStart(2, "0")}:${time.getMinutes().toString().padStart(2, "0")}]`
    },
    "onMessage": function(msg)
    {
      if (msg.display_msg !== undefined)
      {
        const disp_msg = {
          "id": Math.floor(Math.random() * 100000000),
          "time": new Date(),
          "text": msg.display_msg
        };
        model.messages.push(disp_msg);

        if (model.messages.length > 10)
        {
          model.messages.shift();
        }
      }
    }
  }
}
</script>