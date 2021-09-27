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
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "Home",
	data() {
		return {
			
		};
	},
	components: {

	},
	mounted() {
		document.title = "Accueil | Communoservice";
	},
	methods: {

	},
};
</script>
