<template>
	<div class="card mb-3 h-140">
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
				Réservé pour le : {{ reservedOffer.reservation_date }}</time
			>

			<!-- <div class="is-flex is-flex-wrap-wrap is-justify-content-space-between"> -->
			<div class="is-flex is-flex-wrap-wrap is-justify-content-end mt-4">
				<!-- <time
					class="is-align-self-center"
					datetime="2016-1-1"
					v-if="reservedOffer.reservation_date"
				>
					Réservé pour le : {{ reservedOffer.reservation_date }}</time
				> -->
				<button class="button is-success w-100 mr-2">
					Terminer
				</button>
				<button class="button is-danger w-100">
					Annuler
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "ReservedOffer",
	props: {
		reservedOffer: Object,
	},
};
</script>
