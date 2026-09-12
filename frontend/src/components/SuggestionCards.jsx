const SUGGESTIONS = [
  {
    title: "Verify a customer",
    example: "My account email is aaron.mitchell@chinookcorp.com",
  },
  {
    title: "Explore an artist",
    example: "What albums do you have by The Rolling Stones?",
  },
  {
    title: "Resolve an invoice",
    example: "What was my most recent purchase? My customer ID is 10.",
  },
];

export default function SuggestionCards({ onPick }) {
  return (
    <div className="max-w-lg mx-auto w-full mt-6 space-y-3">
      {SUGGESTIONS.map((s) => (
        <button
          key={s.title}
          onClick={() => onPick(s.example)}
          className="w-full text-left bg-surface border border-line rounded-xl2 px-5 py-4 hover:border-teal/50 hover:shadow-panel transition-all group"
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-forest2">{s.title}</span>
            <svg
              viewBox="0 0 24 24"
              className="h-4 w-4 text-faint group-hover:text-teal transition-colors"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
            >
              <path d="M7 17L17 7M9 7h8v8" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <p className="text-sm text-muted mt-1">{s.example}</p>
        </button>
      ))}
    </div>
  );
}
