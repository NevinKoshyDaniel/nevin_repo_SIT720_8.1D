<!-- frontend/src/routes/+page.svelte -->
<script lang="ts">
    // Using Svelte 5 runes for reactive state management
    let suburb = $state("Blacktown");
    let property_type = $state("House");
    let bedrooms = $state(3);
    let bathrooms = $state(2);
    let car_spaces = $state(1);
    let land_size_sqm = $state(450);
    
    let predictedPrice = $state<number | null>(null);
    let isLoading = $state(false);
    let errorMessage = $state("");

    const suburbs = ["Blacktown", "St Ives", "Vaucluse"];
    const propertyTypes = ["House", "Townhouse", "Unit", "Apartment"];

    async function handlePredict() {
        isLoading = true;
        errorMessage = "";
        predictedPrice = null;

        const payload = {
            suburb,
            property_type,
            bedrooms,
            bathrooms,
            car_spaces,
            land_size_sqm: land_size_sqm || null
        };

        try {
            const response = await fetch("http://localhost:8000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Failed to fetch prediction");
            
            const data = await response.json();
            predictedPrice = data.predicted_price;
        } catch (error) {
            errorMessage = "Inference failed. Ensure the FastAPI backend is running.";
        } finally {
            isLoading = false;
        }
    }
</script>

<main class="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
    <div class="max-w-xl w-full bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">Automated Valuation Model</h1>
        <p class="text-slate-500 mb-8">Sydney Housing Price Prediction System</p>

        <form onsubmit={(e) => { e.preventDefault(); handlePredict(); }} class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col gap-1">
                    <label class="text-sm font-semibold text-slate-700" for="suburb">Suburb</label>
                    <select id="suburb" bind:value={suburb} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none">
                        {#each suburbs as sub}
                            <option value={sub}>{sub}</option>
                        {/each}
                    </select>
                </div>

                <div class="flex flex-col gap-1">
                    <label class="text-sm font-semibold text-slate-700" for="property_type">Property Type</label>
                    <select id="property_type" bind:value={property_type} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none">
                        {#each propertyTypes as pt}
                            <option value={pt}>{pt}</option>
                        {/each}
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
                <div class="flex flex-col gap-1">
                    <label class="text-sm font-semibold text-slate-700" for="beds">Beds</label>
                    <input id="beds" type="number" min="0" bind:value={bedrooms} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none" required />
                </div>
                <div class="flex flex-col gap-1">
                    <label class="text-sm font-semibold text-slate-700" for="baths">Baths</label>
                    <input id="baths" type="number" min="0" bind:value={bathrooms} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none" required />
                </div>
                <div class="flex flex-col gap-1">
                    <label class="text-sm font-semibold text-slate-700" for="cars">Cars</label>
                    <input id="cars" type="number" min="0" bind:value={car_spaces} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none" required />
                </div>
            </div>

            <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold text-slate-700" for="land">Land Size (sqm)</label>
                <input id="land" type="number" min="0" bind:value={land_size_sqm} class="p-3 rounded-lg border border-slate-200 bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Leave empty if apartment" />
            </div>

            <button type="submit" disabled={isLoading} class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:bg-blue-300">
                {isLoading ? 'Running Model...' : 'Predict Value'}
            </button>
        </form>

        {#if errorMessage}
            <div class="mt-6 p-4 bg-red-50 text-red-700 rounded-lg border border-red-100">
                {errorMessage}
            </div>
        {/if}

        {#if predictedPrice !== null}
            <div class="mt-8 p-6 bg-emerald-50 rounded-xl border border-emerald-100 text-center animate-fade-in">
                <p class="text-emerald-700 font-semibold mb-1">Estimated Market Value</p>
                <p class="text-4xl font-extrabold text-emerald-900">
                    ${predictedPrice.toLocaleString('en-AU', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                </p>
            </div>
        {/if}
    </div>
</main>

<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in {
        animation: fadeIn 0.4s ease-out forwards;
    }
</style>