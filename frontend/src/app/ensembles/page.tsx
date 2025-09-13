'use client';

import { useEffect, useState } from 'react';
import api from '@/services/api';
import { Ensemble } from '@/types/ensemble';


export default function EnsemblesPage() {
    const [ensembles, setEnsembles] = useState<Ensemble[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchEnsembles = async () => {
            try {
                const response = await api.get('/ensembles/');
                setEnsembles(response.data);
            } catch (err) {
                setError('Failed to fetch ensembles.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchEnsembles();
    }, []);

    if (loading) {
        return <p className="text-center mt-4">Loading...</p>;
    }

    if (error) {
        return <p className="text-center mt-4 text-red-500">{error}</p>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Ensembles</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {ensembles.map((ensemble) => (
                    <div key={ensemble.id} className="border p-4 rounded-lg shadow">
                        <h2 className="text-xl font-semibold">{ensemble.name}</h2>
                        <p className="text-gray-600">{ensemble.type.replace(/_/g, ' ')}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
