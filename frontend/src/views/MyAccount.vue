<template>
	<div class="page-my-account">

		<div class="is-flex">
			<figure class="image is-128x128 round-shadow has-image-centered">
				<img class="is-rounded" src="https://axim-auto.fr/wp-content/uploads/2019/09/0_200.png">
				<figcaption class="has-text-centered">[nom ici]</figcaption>
			</figure>
		</div>
		<!--
		<div class="tabs is-medium mt-6 is-boxed">
			<ul>
				<li v-bind:class="{ 'is-active': isActive == 'my-services'}"><a v-on:click="isActive = 'my-services'" class="w-200">Mes services</a></li>
				<li v-bind:class="{ 'is-active': isActive == 'create-service'}"><a v-on:click="isActive = 'create-service'" class="w-200">Créer un service</a></li>
				<li v-bind:class="{ 'is-active': isActive == 'completed-services'}"><a v-on:click="isActive = 'completed-services'" class="w-200">Services complétés</a></li>
			</ul>
		</div>-->
		<div class="columns mt-6">
			<div class="column">
				<div class="box">
					<h3 class="test-classe">Créer un service</h3>

					<div class="field">
						<label class="label">Type de service</label>
						<div class="control">
							<div class="select">
								<select class="w-200">
									<option>Tonte de pelouse</option>
									<option>Déneigement</option>
								</select>
							</div>
						</div>
					</div>
					<div class="field">
						<label class="label">Type de compensation</label>
						<div class="control">
							<div class="select">
								<select class="w-200">
									<option>Taux horaire</option>
									<option>Taux fixe</option>
								</select>
							</div>
						</div>
					</div>

					<label class="label">Montant offert</label>
					<div class="field has-addons">

						<p class="control">
							<span class="select">
								<select>
									<option>$</option>
									<option>£</option>
									<option>€</option>
								</select>
							</span>
						</p>
						<p class="control">
							<input class="input" type="text" placeholder="Montant">
						</p>
					</div>

					<div class="field">
						<label class="label">Message</label>
						<div class="control">
							<textarea class="textarea" placeholder="Textarea"></textarea>
						</div>
					</div>

					<div class="field">
						<div class="control">
							<label class="checkbox">
								<input type="checkbox">
								J'accepte les <a href="#">termes et conditions</a>
							</label>
						</div>
					</div>

					<div class="columns is-centered mt-5">
						<div class="column control is-half">
							<button class="button is-success w-200"
								v-on:click="modalCreateisActive = 'on'">Créer</button>
						</div>
					</div>
				</div>
			</div>

			<div class="column">
				<div class="box">
					<h3 class="test-classe">Mes services actifs</h3>
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
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
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
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
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
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
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
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
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
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
				</div>
			</div>

			<div class="column">
				<div class="box">
					<h3 class="test-classe">Historique</h3>
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
									<p class="subtitle is-6">Location ici</p>
								</div>
							</div>

							<div class="columns">
								<div class="column is-half">
									<time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
								</div>
								<div class="column is-half">
									<span class="icon-text has-text-success">
										<span class="icon">
											<i class="fas fa-check-square"></i>
										</span>
										<span>Complété</span>
									</span>
								</div>
							</div>
						</div>
					</div>
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
									<p class="subtitle is-6">Location ici</p>
								</div>
							</div>
							<div class="columns">
								<div class="column is-half">
									<time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
								</div>
								<div class="column is-half">
									<span class="icon-text has-text-warning">
										<span class="icon">
											<i class="fas fa-exclamation-triangle"></i>
										</span>
										<span>Cancelé</span>
									</span>
								</div>
							</div>
						</div>
					</div>
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
									<p class="subtitle is-6">Location ici</p>
								</div>
							</div>
							<div class="columns">
								<div class="column is-half">
									<time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
								</div>
								<div class="column is-half">
									<span class="icon-text has-text-success">
										<span class="icon">
											<i class="fas fa-check-square"></i>
										</span>
										<span>Complété</span>
									</span>
								</div>
							</div>
						</div>
					</div>
					<div class="card mb-3 h-140">
						<div class="card-content">
							<div class="media">
								<div class="media-left">
									<figure class="image is-48x48">
										<img src="https://bulma.io/images/placeholders/96x96.png"
											alt="Placeholder image">
									</figure>
								</div>
								<div class="media-content">
									<p class="title is-4">Type de service</p>
									<p class="subtitle is-6">Location ici</p>
								</div>
							</div>
							<div class="columns">
								<div class="column is-half">
									<time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
								</div>
								<div class="column is-half">
									<span class="icon-text has-text-danger">
										<span class="icon">
											<i class="fas fa-ban"></i>
										</span>
										<span>Non complété</span>
									</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<span class="icon-text has-text-danger">
			<span class="icon">
				<i class="fas fa-arrow-right-from-bracket"></i>
			</span>
		</span>

		<div class="modal" v-bind:class="{ 'is-active': modalCreateisActive == 'on'}">
			<div class="modal-background"></div>
			<div class="modal-card">
				<header class="modal-card-head">
					<p class="modal-card-title">Confirmation</p>
					<button class="delete" v-on:click="modalCreateisActive = 'off'" aria-label="close"></button>
				</header>
				<section class="modal-card-body">
					Êtes-vous certain de vouloir créer ce service?
				</section>
				<footer class="modal-card-foot">
					<button class="button is-danger w-100" v-on:click="modalCreateisActive = 'off'">Non</button>
					<button class="button is-success w-100">Oui</button>
				</footer>
			</div>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	export default {
		name: "MyAccount",
		data() {
			return {
				orders: [],
				modalCreateisActive: 'off',
			};
		},
		mounted() {
			document.title = "Mon compte | Communoservice";
		},
		methods: {

		},
	};
</script>

// <style lang="sass" scoped>
	// @import "../../node_modules/bulmaswatch/minty/bulmaswatch.scss";

	// .test-classe {
	// 	@extend .title;
	// 	@extend .is-4;
	// 	@extend .has-text-centered;
	// }
	// 
</style>