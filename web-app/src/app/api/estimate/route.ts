import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const formData = await request.formData();
        const category = formData.get('category');
        const karat = formData.get('karat');
        const image = formData.get('image');

        if (!category || !karat || !image) {
            return NextResponse.json({ success: false, error: 'Missing required fields' }, { status: 400 });
        }

        // Forward to FastAPI Backend
        const backendFormData = new FormData();

        const imageFile = image as File;
        const arrayBuffer = await imageFile.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);
        const blob = new Blob([buffer], { type: imageFile.type });

        backendFormData.append('image', blob, imageFile.name);
        backendFormData.append('category', category as string);
        backendFormData.append('purity', karat as string); // Backend expects 'purity'

        const backendResponse = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: backendFormData,
        });

        if (!backendResponse.ok) {
            const errorText = await backendResponse.text();
            throw new Error(`Backend API error: ${backendResponse.status} ${errorText}`);
        }

        const backendResult = await backendResponse.json();

        if (!backendResult.success) {
            throw new Error('Backend returned failure');
        }

        const { gold_weight_g, diamond_weight_ct } = backendResult.data;

        // Valuation Logic
        const CURRENT_GOLD_PRICE_PER_GRAM_24K = 7500; // Approx Market Rate
        const DIAMOND_PRICE_PER_CT = 35000;

        const purityFactor = parseInt(karat as string) / 24;
        const goldValue = gold_weight_g * CURRENT_GOLD_PRICE_PER_GRAM_24K * purityFactor;
        const stoneValue = diamond_weight_ct * DIAMOND_PRICE_PER_CT;
        const totalValue = goldValue + stoneValue;

        return NextResponse.json({
            success: true,
            data: {
                estimated_value: Math.round(totalValue),
                gold_weight: gold_weight_g,
                diamond_weight: diamond_weight_ct,
                breakdown: {
                    gold_value: Math.round(goldValue),
                    stone_value: Math.round(stoneValue)
                },
                currency: 'INR'
            }
        });

    } catch (error) {
        console.error("Estimate API Error:", error);
        return NextResponse.json({ success: false, error: 'Estimation failed: ' + (error as Error).message }, { status: 500 });
    }
}
