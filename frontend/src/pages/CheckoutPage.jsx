import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function CheckoutPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [paying, setPaying] = useState(false);
    const [error, setError] = useState("");
    const [showSimulatedModal, setShowSimulatedModal] = useState(false);

    useEffect(() => {
        const fetchOrder = async () => {
            try {
                const res = await api.get("/orders/my");
                const found = res.data.find(
                    (o) => String(o._id) === String(orderId) || String(o.id) === String(orderId)
                );
                if (!found) throw new Error("Order not found");
                setOrder(found);
            } catch {
                setError("Could not load order details.");
            } finally {
                setLoading(false);
            }
        };
        fetchOrder();
    }, [orderId]);

    const handleInitiatePayment = () => {
        setError("");
        setShowSimulatedModal(true);
    };

    const handleConfirmSimulatedPayment = async () => {
        setPaying(true);
        setError("");

        try {
            // Step 1: Request simulated payment order
            const createRes = await api.post("/payment/create-order", { orderId });
            const data = createRes.data;

            // Simulated transaction delay (1.2 seconds) for realistic UI experience
            await new Promise((resolve) => setTimeout(resolve, 1200));

            // Step 2: Verify simulated payment
            await api.post("/payment/verify", {
                razorpay_order_id: data.razorpayOrderId,
                razorpay_payment_id: `pay_simulated_${Date.now()}`,
                razorpay_signature: "simulated_lab_signature",
                orderId,
            });

            setShowSimulatedModal(false);
            navigate(`/payment-success/${orderId}`);
        } catch (err) {
            setError(err.response?.data?.message || "Simulated payment failed. Please try again.");
            setPaying(false);
        }
    };

    if (loading)
        return (
            <div className="flex min-h-screen items-center justify-center bg-[#f1f8f5] dark:bg-[#0f1a18]">
                <p className="text-sm text-[#173f3b] dark:text-slate-400">Loading order...</p>
            </div>
        );

    if (error && !order)
        return (
            <div className="flex min-h-screen items-center justify-center bg-[#f1f8f5] dark:bg-[#0f1a18]">
                <p className="text-red-500 dark:text-red-400">{error}</p>
            </div>
        );

    const plan = order?.planId;

    return (
        <div className="flex min-h-screen items-center justify-center bg-[#f1f8f5] px-4 py-16 dark:bg-[#0f1a18]">
            <div className="w-full max-w-md overflow-hidden rounded-2xl border border-emerald-900/10 bg-white shadow-[0_12px_35px_rgba(32,75,67,0.06)] dark:bg-[#1a2e2b] dark:border-white/10 dark:shadow-none">
                {/* Header */}
                <div className="bg-[#173f3b] px-8 py-6 dark:bg-[#0d2420]">
                    <div className="flex items-center justify-between mb-1">
                        <p className="text-xs uppercase tracking-widest text-[#dcefeb] dark:text-emerald-300">MealMitra</p>
                        <span className="text-[11px] font-semibold bg-emerald-500/20 text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                            Demo Mode
                        </span>
                    </div>
                    <h1 className="text-2xl font-semibold text-white">Order Summary</h1>
                </div>

                {/* Plan details */}
                <div className="px-8 py-6">
                    <div className="flex items-start justify-between">
                        <div>
                            <p className="mb-1 text-xs uppercase tracking-wide text-slate-400 dark:text-slate-500">Plan</p>
                            <p className="text-lg font-semibold text-[#173f3b] dark:text-emerald-100">{plan?.title}</p>
                        </div>
                        <span className="rounded-full bg-[#dcefeb] px-3 py-1 text-xs font-medium text-[#173f3b] dark:bg-emerald-900/40 dark:text-emerald-300">
                            {plan?.mealType}
                        </span>
                    </div>

                    <div className="my-6 border-t border-emerald-900/10 dark:border-white/10" />

                    <div className="space-y-6">
                        <InfoRow label="Duration" value={plan?.duration} />
                        <InfoRow label="Description" value={plan?.description} stacked />
                    </div>

                    <div className="my-6 border-t border-emerald-900/10 dark:border-white/10" />

                    <div className="flex items-center justify-between">
                        <p className="text-sm text-slate-500 dark:text-slate-400">Total payable</p>
                        <p className="text-2xl font-bold text-[#173f3b] dark:text-emerald-200">₹{plan?.price}</p>
                    </div>
                </div>

                {/* CTA */}
                <div className="px-8 pb-8">
                    {error && (
                        <p className="mb-3 text-center text-sm text-red-500 dark:text-red-400">{error}</p>
                    )}
                    <button
                        onClick={handleInitiatePayment}
                        disabled={paying}
                        className="w-full rounded-xl bg-[#e9827c] py-3 font-semibold text-white transition-colors duration-200 hover:bg-[#d9726c] disabled:opacity-60 cursor-pointer"
                    >
                        Pay ₹{plan?.price} (Simulated)
                    </button>
                    <p className="mt-3 text-center text-xs text-slate-400 dark:text-slate-500">
                        Demonstration flow · Simulated payment without actual charges
                    </p>
                </div>
            </div>

            {/* Simulated Payment Modal */}
            {showSimulatedModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
                    <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl dark:bg-[#1a2e2b] dark:border dark:border-white/10">
                        <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-white/10">
                            <h3 className="font-semibold text-slate-800 dark:text-white">Simulated Payment Gateway</h3>
                            <button
                                onClick={() => !paying && setShowSimulatedModal(false)}
                                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg leading-none"
                            >
                                &times;
                            </button>
                        </div>
                        <div className="py-4 space-y-3">
                            <div className="rounded-lg bg-emerald-50 dark:bg-emerald-950/40 p-3 text-xs text-emerald-800 dark:text-emerald-200 border border-emerald-200 dark:border-emerald-800/40">
                                <span className="font-semibold">Lab Demonstration Mode:</span> This is a mock payment flow created to fulfill Full Stack Development Lab requirements. No real payment gateway is contacted.
                            </div>
                            <div className="flex justify-between text-sm py-2">
                                <span className="text-slate-500 dark:text-slate-400">Merchant:</span>
                                <span className="font-medium text-slate-800 dark:text-slate-200">MealMitra Tiffin Service</span>
                            </div>
                            <div className="flex justify-between text-sm py-1">
                                <span className="text-slate-500 dark:text-slate-400">Order Plan:</span>
                                <span className="font-medium text-slate-800 dark:text-slate-200">{plan?.title}</span>
                            </div>
                            <div className="flex justify-between text-sm py-1 border-t border-slate-100 dark:border-white/10 pt-2">
                                <span className="font-semibold text-slate-700 dark:text-slate-300">Amount:</span>
                                <span className="font-bold text-lg text-emerald-600 dark:text-emerald-400">₹{plan?.price}</span>
                            </div>
                        </div>
                        <div className="flex gap-2 pt-2">
                            <button
                                onClick={() => setShowSimulatedModal(false)}
                                disabled={paying}
                                className="flex-1 py-2.5 rounded-xl border border-slate-200 text-slate-600 dark:border-white/10 dark:text-slate-300 text-sm font-medium hover:bg-slate-50 dark:hover:bg-white/5 transition"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleConfirmSimulatedPayment}
                                disabled={paying}
                                className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium transition flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
                            >
                                {paying ? (
                                    <>
                                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                                        <span>Processing...</span>
                                    </>
                                ) : (
                                    "Confirm Demo Payment"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

function InfoRow({ label, value, stacked = false }) {
    return (
        <div className={stacked ? "" : "flex items-baseline gap-3"}>
            <span className="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">
                {label}
            </span>
            <span
                className={
                    stacked
                        ? "mt-3 block max-w-[85%] text-sm font-semibold leading-relaxed text-[#173f3b] dark:text-slate-200"
                        : "text-sm font-semibold text-[#173f3b] dark:text-slate-200"
                }
            >
                {value}
            </span>
        </div>
    );
}
