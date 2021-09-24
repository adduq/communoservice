<template>
	<div class="home">
		<section class="hero is-medium is-dark mb-6">
			<div class="hero-body has-text-centered">
				<p class="title mb-6">Bienvenue sur Communoservice</p>
				<p class="subtitle">Le meilleur site pour les services communautaires</p>
			</div>
		</section>

		<div class="columns is-multiline is-12">
			<div class="column is-12">
				<h2 class="is-size-2 has-text-centered">
					Liste des services
				</h2>
			</div>
		</div>
		<div class="columns mt-6">
			<div class="column">
				<div class="box">

				</div>
			</div>
			<div class="column is-two-thirds">
				<div class="box">

          <DetailedOffer
            v-for="offer in offers"
            v-bind:key="offer.id"
            v-bind:offer="offer"
          />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
import DetailedOffer from "@/components/DetailedOffer";
	export default {
		name: "Home",
		data() {
			return {
				offers: [],
			};
		},
		components: {
DetailedOffer
		},
		mounted() {
			document.title = "Accueil | Communoservice";
			this.getAllOffers();
		},
		methods: {
			    async getAllOffers(){
      this.$store.commit("setIsLoading", true);
      
      await axios
        .get("/api/v1/offers/")
        .then((response) => {
          this.offers = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    }
		},
	};
</script>