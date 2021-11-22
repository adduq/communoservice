<template>
	<!-- <a href="#"> -->
		<div class="card mb-3 h-140" :class="accountPage ? '' : 'is-pointer-cursor'">
			<div class="card-content">
				<div class="media">
					<div class="media-left">
						<figure class="image is-64x64">
							<img
								class="is-rounded"
								src="https://axim-auto.fr/wp-content/uploads/2019/09/0_200.png"
							/>
						</figure>
					</div>
					<div class="media-content is-clipped">
						<p class="title is-4">{{ offer.type_service }}</p>
						<p class="subtitle is-6">
							{{
								offer.description.length >= 50
									? offer.description.substring(0, 50) + "..."
									: offer.description
							}}
						</p>
					</div>
				</div>


				<div class="has-text-danger" v-if="offer.end_date != null">
					<time datetime="{{offer.end_date}}">
						Valide jusqu'au {{ offer.end_date }}
					</time>
				</div>

				<div class="is-family-monospace is-flex is-justify-content-flex-end mt-3"
					:class="accountPage ? '' : 'is-size-4-desktop'">
					<span
						class="tag is-rounded"
						:class="offer.monday ? 'is-info' : 'is-dark'"
					>
						L
					</span>
					<span
						class="tag is-rounded"
						:class="offer.tuesday ? 'is-info' : 'is-dark'"
					>
						M
					</span>
					<span
						class="tag is-rounded"
						:class="offer.wednesday ? 'is-info' : 'is-dark'"
					>
						M
					</span>
					<span
						class="tag is-rounded"
						:class="offer.thursday ? 'is-info' : 'is-dark'"
					>
						J
					</span>
					<span
						class="tag is-rounded"
						:class="offer.friday ? 'is-info' : 'is-dark'"
					>
						V
					</span>
					<span
						class="tag is-rounded"
						:class="offer.saturday ? 'is-info' : 'is-dark'"
					>
						S
					</span>
					<span
						class="tag is-rounded"
						:class="offer.sunday ? 'is-info' : 'is-dark'"
					>
						D
					</span>
				</div>


				<!-- <div class="columns has-text-danger">
					<div class="column" v-if="offer.end_date != null">
						<time datetime="{{offer.end_date}}">
							Valide jusqu'au {{ offer.end_date }}
						</time>
					</div>
					<div
						class="column is-flex is-justify-content-flex-end is-family-monospace"
					>
						<span
							class="tag is-rounded"
							:class="offer.monday ? 'is-info' : 'is-dark'"
						>
							L
						</span>
						<span
							class="tag is-rounded"
							:class="offer.tuesday ? 'is-info' : 'is-dark'"
						>
							M
						</span>
						<span
							class="tag is-rounded"
							:class="offer.wednesday ? 'is-info' : 'is-dark'"
						>
							M
						</span>
						<span
							class="tag is-rounded"
							:class="offer.thursday ? 'is-info' : 'is-dark'"
						>
							J
						</span>
						<span
							class="tag is-rounded"
							:class="offer.friday ? 'is-info' : 'is-dark'"
						>
							V
						</span>
						<span
							class="tag is-rounded"
							:class="offer.saturday ? 'is-info' : 'is-dark'"
						>
							S
						</span>
						<span
							class="tag is-rounded"
							:class="offer.sunday ? 'is-info' : 'is-dark'"
						>
							D
						</span>
					</div>
				</div> -->

				<div v-if="accountPage" class="is-flex is-justify-content-center mt-4">
					<button class="button is-danger w-200" v-on:click="deleteOffer">
						Supprimer
					</button>
				</div>
			</div>
		</div>
	<!-- </a> -->
</template>

<script>
import axios from "axios";

export default {
	name: "DetailedOffer",
	props: {
		offer: Object,
		accountPage: false,
	},
	// mounted() {
	// 	if (!this.accountPage) {
	// 		document.getElementsByClassName('.card')
	// 	}
	// },
	methods: {
		async deleteOffer() {
			await axios
				.delete(
					`/api/v1/active-offers/${this.offer.id_active_offer}/`
				)
				.then((res) => {
					this.$parent.getAllOffers(this.offer.user);
					this.$parent.getReservedOffersForUser(this.offer.user);
				})
				.catch((err) => {
					console.log(err);
				});
		},
	}
};
</script>

<style scoped>
.is-pointer-cursor {
	cursor: pointer;
}
</style>