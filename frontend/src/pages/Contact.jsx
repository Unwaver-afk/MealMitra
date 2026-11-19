import { useState } from "react";
import api from "../services/api";
import { useToast } from "../context/useToast";

const contactDetails = [
    { label: "Contact person", value: "Prakhar Agnihotri",              detail: "Customer care coordinator" },
    { label: "Email",          value: "hello@mealmitra.example",     detail: "Replies within one business day", href: "mailto:hello@mealmitra.example" },
    { label: "Mobile",         value: "+91 90000 12345",             detail: "Monday to Saturday, 9 AM–7 PM",   href: "tel:+919000012345" },
    { label: "Address",        value: "Random Office, Noida , Uttar Pradesh , India", detail: "Noida ,UP ,201309" },
];

function Contact() {
    const { toast } = useToast();
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        subject: "",
        message: "",
    });
    const [submitting, setSubmitting] = useState(false);
    const [submitted, setSubmitted] = useState(false);
    const [formErrors, setFormErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
        if (formErrors[name]) {
            setFormErrors((prev) => ({ ...prev, [name]: null }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setFormErrors({});

        try {
            const res = await api.post("/contact/", formData);
            if (res.data?.success) {
                toast.success("Thank you! Your message has been submitted to the Django backend.");
                setSubmitted(true);
                setFormData({ name: "", email: "", subject: "", message: "" });
            }
        } catch (err) {
            if (err.response?.data?.errors) {
                setFormErrors(err.response.data.errors);
            } else {
                toast.error("Failed to send message. Please try again.");
            }
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <main className="min-h-screen bg-[#f1f8f5] text-slate-800 dark:bg-[#0f1a18] dark:text-slate-100">
            {/* Hero */}
            <section className="relative overflow-hidden border-b border-emerald-900/10 bg-[#dcefeb] px-5 py-16 sm:px-8 sm:py-20 dark:bg-[#0d2420] dark:border-white/10">
                <div className="absolute -right-24 -top-28 h-80 w-80 rounded-full border-[44px] border-white/45 dark:border-white/10" />
                <div className="absolute bottom-8 right-[18%] h-3 w-20 rounded-full bg-[#e9827c] opacity-80" />
                <div className="relative mx-auto max-w-6xl">
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-800 dark:text-emerald-400">Contact MealMitra</p>
                    <h1 className="mt-5 max-w-3xl text-4xl font-semibold leading-tight tracking-tight text-[#173f3b] sm:text-5xl dark:text-emerald-100">
                        Thoughtful support for healthier everyday meals.
                    </h1>
                    <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600 dark:text-slate-300">
                        Questions about subscriptions, delivery schedules, or meal plans? Our team is here to make things clear and simple.
                    </p>
                </div>
            </section>

            <section className="mx-auto grid max-w-6xl gap-8 px-5 py-12 sm:px-8 lg:grid-cols-[1fr_360px] lg:py-16">
                <div className="space-y-10">
                    <div>
                        <div className="mb-7 flex items-end justify-between border-b border-emerald-900/15 pb-4 dark:border-white/10">
                            <div>
                                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700 dark:text-emerald-400">Reach us</p>
                                <h2 className="mt-2 text-2xl font-semibold text-[#173f3b] dark:text-emerald-100">Contact information</h2>
                            </div>
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">
                            {contactDetails.map((item, index) => (
                                <article key={item.label} className="rounded-2xl border border-emerald-900/10 bg-white p-6 shadow-[0_12px_35px_rgba(32,75,67,0.06)] dark:bg-[#1a2e2b] dark:border-white/10 dark:shadow-none">
                                    <div className="mb-8 flex items-center justify-between">
                                        <span className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700 dark:text-emerald-400">
                                            {item.label}
                                        </span>
                                        <span className="font-mono text-xs text-slate-300 dark:text-slate-600">0{index + 1}</span>
                                    </div>
                                    {item.href ? (
                                        <a href={item.href} className="text-lg font-semibold text-[#173f3b] underline decoration-emerald-200 underline-offset-4 transition hover:decoration-[#e9827c] dark:text-emerald-200 dark:decoration-emerald-700">
                                            {item.value}
                                        </a>
                                    ) : (
                                        <p className="text-lg font-semibold text-[#173f3b] dark:text-emerald-100">{item.value}</p>
                                    )}
                                    <p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">{item.detail}</p>
                                </article>
                            ))}
                        </div>
                    </div>

                    {/* Interactive Django ModelForm Submission */}
                    <div className="rounded-2xl border border-emerald-900/10 bg-white p-7 shadow-[0_12px_35px_rgba(32,75,67,0.06)] dark:bg-[#1a2e2b] dark:border-white/10 dark:shadow-none">
                        <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100 dark:border-white/10">
                            <div>
                                <h3 className="text-xl font-semibold text-[#173f3b] dark:text-emerald-100">Send an Inquiry</h3>
                                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Validated by Django ModelForms & saved in SQLite</p>
                            </div>
                            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
                                Module 4 Demo
                            </span>
                        </div>

                        {submitted && (
                            <div className="mb-6 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-200 border border-emerald-200 dark:border-emerald-800/40">
                                ✓ Message received! Our team will respond shortly.
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid gap-4 sm:grid-cols-2">
                                <div>
                                    <label className="block text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                                        Your Name
                                    </label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        required
                                        placeholder="Prakhar Agnihotri"
                                        className="h-11 w-full rounded-xl border border-emerald-900/10 bg-[#f8faf9] px-4 text-sm text-slate-700 outline-none focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10 dark:border-white/10 dark:bg-[#0f1a18] dark:text-slate-100"
                                    />
                                    {formErrors.name && (
                                        <p className="mt-1 text-xs text-red-500">{formErrors.name.join(" ")}</p>
                                    )}
                                </div>
                                <div>
                                    <label className="block text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                                        Email Address
                                    </label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                        placeholder="name@example.com"
                                        className="h-11 w-full rounded-xl border border-emerald-900/10 bg-[#f8faf9] px-4 text-sm text-slate-700 outline-none focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10 dark:border-white/10 dark:bg-[#0f1a18] dark:text-slate-100"
                                    />
                                    {formErrors.email && (
                                        <p className="mt-1 text-xs text-red-500">{formErrors.email.join(" ")}</p>
                                    )}
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                                    Subject
                                </label>
                                <input
                                    type="text"
                                    name="subject"
                                    value={formData.subject}
                                    onChange={handleChange}
                                    placeholder="Subscription / Delivery Query"
                                    className="h-11 w-full rounded-xl border border-emerald-900/10 bg-[#f8faf9] px-4 text-sm text-slate-700 outline-none focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10 dark:border-white/10 dark:bg-[#0f1a18] dark:text-slate-100"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                                    Message
                                </label>
                                <textarea
                                    name="message"
                                    rows="4"
                                    value={formData.message}
                                    onChange={handleChange}
                                    required
                                    placeholder="Tell us what you need help with..."
                                    className="w-full rounded-xl border border-emerald-900/10 bg-[#f8faf9] p-4 text-sm text-slate-700 outline-none focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10 dark:border-white/10 dark:bg-[#0f1a18] dark:text-slate-100"
                                />
                                {formErrors.message && (
                                    <p className="mt-1 text-xs text-red-500">{formErrors.message.join(" ")}</p>
                                )}
                            </div>
                            <button
                                type="submit"
                                disabled={submitting}
                                className="rounded-xl bg-[#173f3b] px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-[#0f2e2b] dark:bg-emerald-600 dark:hover:bg-emerald-500 cursor-pointer disabled:opacity-60"
                            >
                                {submitting ? "Submitting..." : "Send Message to Django Backend"}
                            </button>
                        </form>
                    </div>
                </div>

                <aside className="h-fit rounded-2xl bg-[#173f3b] p-7 text-white shadow-xl shadow-emerald-950/10 lg:sticky lg:top-8 dark:bg-[#0d2420] dark:border dark:border-white/10 dark:shadow-none">
                    <div className="mb-8 flex items-center justify-between">
                        <span className="h-2.5 w-2.5 rounded-full bg-[#e9827c]" />
                        <span className="text-xs font-medium uppercase tracking-[0.18em] text-emerald-200">Support desk</span>
                    </div>
                    <h2 className="text-2xl font-semibold tracking-tight">Need a quick answer?</h2>
                    <p className="mt-3 text-sm leading-6 text-emerald-50/75">Email is best for subscription changes. Call us for same-day delivery questions.</p>
                    <div className="my-7 border-t border-white/15" />
                    <dl className="space-y-5 text-sm">
                        <div><dt className="text-emerald-200">Response time</dt><dd className="mt-1 font-medium">Within 24 hours</dd></div>
                        <div><dt className="text-emerald-200">Service region</dt><dd className="mt-1 font-medium">Noida and nearby sectors</dd></div>
                        <div><dt className="text-emerald-200">Office hours</dt><dd className="mt-1 font-medium">Mon–Sat · 9:00 AM–7:00 PM</dd></div>
                    </dl>
                    <a href="mailto:hello@mealmitra.example" className="mt-8 block rounded-xl bg-white px-5 py-3.5 text-center text-sm font-semibold text-[#173f3b] transition hover:bg-emerald-50">
                        Write to our team
                    </a>
                    <p className="mt-4 text-center text-xs text-emerald-100/55">THE CONTACT DETAILS ARE CURRENTLY DEMO ONLY</p>
                </aside>
            </section>
        </main>
    );
}

export default Contact;
