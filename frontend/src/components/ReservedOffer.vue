<template>
	<div class="card mb-3 h-140" v-if="reservedOffer">
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
					<p class="title is-4">{{ reservedOffer.id_offer.type_service }}</p>
					<p class="subtitle is-6">
						{{
							reservedOffer.id_offer.description.length >= 50
								? reservedOffer.id_offer.description.substring(0, 50) + "..."
								: reservedOffer.id_offer.description
						}}
					</p>
				</div>
			</div>

			<time datetime="2016-1-1" v-if="reservedOffer.reservation_date">
				Réservé pour le : {{ reservedOffer.reservation_date }}
			</time>
			<p>
				<!-- TODO: Différencier employé / employeur pour le référent -->
				Référent : {{ reservedOffer.recruiter.first_name }}
				{{ reservedOffer.recruiter.last_name }}
			</p>

			<!-- <div class="is-flex is-flex-wrap-wrap is-justify-content-space-between"> -->
			<div class="is-flex is-flex-wrap-wrap is-justify-content-end mt-4">
				<!-- <time
					class="is-align-self-center"
					datetime="2016-1-1"
					v-if="reservedOffer.reservation_date"
				>
					Réservé pour le : {{ reservedOffer.reservation_date }}</time
				> -->
				<button
					class="button is-success w-100 mr-2"
					v-on:click="terminateOffer"
				>
					Terminer
				</button>
				<button class="button is-danger w-100" v-on:click="cancelOffer">
					Annuler
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";

export default {
	name: "ReservedOffer",
	props: {
		reservedOffer: Object,
	},
	data() {
		return {
			statusDispo: {
				GIVEN: 0,
				NOT_GIVEN: 1,
				CANCEL: 2,
				NO_PRESENCE: 3,
			},
		};
	},
	mounted() {
		console.log(this.reservedOffer ? "True" : "Nope");
	},
	methods: {
		async cancelOffer() {
			this.reservedOffer["status"] = this.statusDispo.CANCEL;
			this.reservedOffer["completed_date"] = new Date()
				.toISOString()
				.split("T")[0];
			this.reservedOffer["id_offer"] = this.reservedOffer.id_offer.id;
			this.reservedOffer[
				"id_active_offer"
			] = this.reservedOffer.id_active_offer.id;
			this.reservedOffer["id_user"] = this.reservedOffer.user.id;
			this.reservedOffer["id_recruiter"] = this.reservedOffer.recruiter.id;

			await axios
				.post("/api/v1/terminated-offers/", this.reservedOffer)
				.then((res) => {
					console.log(res.data);

					this.deleteFromReservedOffer();
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async terminateOffer() {
			alert(this.reservedOffer.recruiter.first_name);
		},
		async deleteFromReservedOffer() {
			await axios
				.delete(
					`/api/v1/reserved-offers/${this.reservedOffer.id}`,
					this.reservedOffer
				)
				.then((res) => {
					console.log(res.data);
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
};
</script>
