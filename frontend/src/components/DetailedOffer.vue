<template>
	<a href="#">
		<div class="card mb-3 h-140">
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
					<div class="media-content">
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

				<div class="columns has-text-danger">
					<div class="column" v-if="offer.expiration_date != null">
						<time datetime="{{offer.expiration_date}}">
							Valide jusqu'au {{ offer.expiration_date }}
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
							:class="offer.thursday ? 'is-info' : 'is-dark'"
						>
							M
						</span>
						<span
							class="tag is-rounded"
							:class="offer.wednesday ? 'is-info' : 'is-dark'"
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
				</div>
			</div>
		</div>
	</a>
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
