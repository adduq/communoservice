<template>
  <div class="card mb-3 h-140">
    <div class="card-content">
      <div class="media">
        <div class="media-left">
          <figure class="image is-48x48">
            <img
              v-bind:src="user_pfp_url"
              @error="this.user_pfp_url = this.MEDIA_URL + 'pfp_default.jpg'"
              onerror='this.src="test"'
              alt="Placeholder image"
            />
          </figure>
        </div>
        <div class="media-content is-clipped">
          <p class="title is-4">{{offer.type_service}}</p>
          <p class="subtitle is-6">Location ici</p>
        </div>
      </div>

      <div class="columns">
        <div class="column">
          <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ActiveOffer",
  props: {
    offer: Object
  },
  data:{
    user_pfp_url: this.MEDIA_URL +"pfp_" + this.offer.user_id + ".jpg"
  }
};
</script>