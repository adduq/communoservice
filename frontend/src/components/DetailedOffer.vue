<template>
  <div class="card mb-3 h-140" v-on:click="modalViewisActive = !modalViewisActive">
    <div class="card-content">
      <div class="media">
        <div class="media-left">
          <figure class="image is-48x48">
            <img
              src="https://bulma.io/images/placeholders/96x96.png"
              alt="Placeholder image"
            />
          </figure>
        </div>
        <div class="media-content">
          <p class="title is-4">{{offer.type_service}}</p>
          <p class="subtitle is-6">Localisation ici</p>
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
  name: "DetailedOffer",
  props: {
        offer: Object
    }
};
</script>

<style lang="scss" scoped>
h1 {
  text-align: center;
}
</style>
