export default function VerifiedContextCard({ customerId }) {
  return (
    <div className="bg-surface border border-line rounded-xl2 p-4">
      <div className="flex items-center gap-2 mb-2">
        <svg viewBox="0 0 24 24" className="h-4 w-4 text-teal" fill="none" stroke="currentColor" strokeWidth="1.8">
          <path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z" strokeLinejoin="round" />
        </svg>
        <span className="text-[11px] font-medium text-faint">Verified context</span>
      </div>

      {customerId ? (
        <p className="text-sm text-ink">
          Customer <span className="font-semibold">#{customerId}</span> is verified for this
          conversation. Billing and catalog agents can use their account data.
        </p>
      ) : (
        <p className="text-sm text-amber">Identity will appear after verification.</p>
      )}
    </div>
  );
}
