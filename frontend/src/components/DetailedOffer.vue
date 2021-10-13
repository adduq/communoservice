<template>
  <div
    class="card mb-3 h-140"
    v-on:click="modalViewisActive = !modalViewisActive"
  >
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
          <p class="title is-4">{{ offer.type_service }}</p>
          <p class="subtitle is-6">{{ offer.description }}</p>
        </div>
      </div>

      <div class="columns has-text-danger">
        <div class="column" v-if="offer.expiration_date == null">
          Valide en tout temps
        </div>
        <div class="column" v-else>
          <time datetime="{{offer.expiration_date}}"
            >Valide jusqu'au {{ offer.expiration_date }}</time
          >
        </div>
      </div>
    </div>
    <div>Disponibilités:</div>
    <span class="button is-rounded is-success" v-if="offer.monday == true">
      Lun
    </span>
    <span class="button is-rounded is-success" v-if="offer.tuesday == true">
      Mar
    </span>
    <span class="button is-rounded is-success" v-if="offer.wednesday == true">
      Mer
    </span>
    <span class="button is-rounded is-success" v-if="offer.thursday == true">
      Jeu
    </span>
    <span class="button is-rounded is-success" v-if="offer.friday == true">
      Ven
    </span>
    <span class="button is-rounded is-success" v-if="offer.saturday == true">
      Sam
    </span>
    <span class="button is-rounded is-success" v-if="offer.sunday == true">
      Dim
    </span>
    <div></div>
  </div>
</template>

<script>
export default {
  name: "DetailedOffer",
  props: {
    offer: Object,
  },
};
</script>

<style lang="scss" scoped>
h1 {
  text-align: center;
}
</style>
