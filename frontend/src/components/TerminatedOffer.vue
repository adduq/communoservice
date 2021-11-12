<template>
	<div class="card mb-3 h-140" v-if="terminatedOffer">
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
					<p class="title is-4">{{ terminatedOffer.id_offer.type_service }}</p>
					<p class="subtitle is-6">
						{{
							terminatedOffer.id_offer.description.length >= 50
								? terminatedOffer.id_offer.description.substring(0, 50) + "..."
								: terminatedOffer.id_offer.description
						}}
					</p>
				</div>
			</div>

			<time
				datetime="2016-1-1"
				v-if="terminatedOffer.status === this.statusDispo.GIVEN"
			>
				Terminé le : {{ terminatedOffer.completed_date }}</time
			>
			<p v-else>L'offre n'a pas été achevée.</p>
			<p>
				Référent : {{ terminatedOffer.recruiter.first_name }}
				{{ terminatedOffer.recruiter.last_name }}
			</p>

			<span
				class="icon-text has-text-success"
				v-if="terminatedOffer.status === this.statusDispo.GIVEN"
			>
				<span class="icon">
					<i class="fas fa-check-square"></i>
				</span>
				<span>Complété</span>
			</span>
			<span
				class="icon-text has-text-warning"
				v-else-if="terminatedOffer.status === this.statusDispo.CANCEL"
			>
				<span class="icon">
					<i class="fas fa-exclamation-triangle"></i>
				</span>
				<span>Annulé</span>
			</span>
			<span class="icon-text has-text-danger" v-else>
				<span class="icon">
					<i class="fas fa-ban"></i>
				</span>
				<span>Non complété</span>
			</span>

			<!-- <div
				class="is-flex is-flex-wrap-wrap is-justify-content-space-between mt-4"
			>
				<time datetime="2016-1-1" v-if="terminatedOffer.completed_date">
					Terminé le : {{ terminatedOffer.completed_date }}</time
				>
				<p v-else>L'offre n'a pas été achevée.</p>
				<p>
					Référent : {{ terminatedOffer.recruiter.first_name }}
					{{ terminatedOffer.recruiter.last_name }}
				</p>
				<span
					class="icon-text has-text-success"
					v-if="terminatedOffer.status === this.statusDispo.GIVEN"
				>
					<span class="icon">
						<i class="fas fa-check-square"></i>
					</span>
					<span>Complété</span>
				</span>
				<span
					class="icon-text has-text-warning"
					v-else-if="terminatedOffer.status === this.statusDispo.CANCEL"
				>
					<span class="icon">
						<i class="fas fa-exclamation-triangle"></i>
					</span>
					<span>Annulé</span>
				</span>
				<span class="icon-text has-text-danger" v-else>
					<span class="icon">
						<i class="fas fa-ban"></i>
					</span>
					<span>Non complété</span>
				</span>
			</div> -->
		</div>
	</div>
</template>

<script>
export default {
	name: "TerminatedOffer",
	props: {
		terminatedOffer: Object,
	},
	data() {
		return {
			statusDispo: {
				GIVEN: 0,
				NOT_GIVEN: 1,
				CANCEL: 2,
				NO_PRESENCE: 3,
			},
			// terminatedOfferKey: 0,
		};
	},
	// methods: {
	// forceRerender() {
	//   this.terminatedOfferKey += 1;
	// }
	// }
};
</script>
