export default function MemoryCard({ memory }) {
  const preferences = memory?.music_preferences || [];

  return (
    <div className="bg-surface border border-line rounded-xl2 p-4">
      <div className="flex items-center gap-2 mb-2">
        <svg viewBox="0 0 24 24" className="h-4 w-4 text-teal" fill="none" stroke="currentColor" strokeWidth="1.8">
          <circle cx="12" cy="12" r="8" />
          <path d="M12 8v4l3 2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <span className="text-[11px] font-medium text-faint">Long-term memory</span>
      </div>

      {preferences.length > 0 ? (
        <>
          <p className="text-sm font-medium text-ink mb-2">Saved preferences</p>
          <div className="flex flex-wrap gap-1.5">
            {preferences.map((p) => (
              <span
                key={p}
                className="text-xs font-medium text-forest2 bg-tealLight px-2.5 py-1 rounded-full"
              >
                {p}
              </span>
            ))}
          </div>
        </>
      ) : (
        <p className="text-sm font-medium text-muted">No preferences yet</p>
      )}
    </div>
  );
}
