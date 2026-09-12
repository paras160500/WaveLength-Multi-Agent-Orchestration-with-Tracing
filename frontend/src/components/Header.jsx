export default function Header({ customerId, agentLabel }) {
  return (
    <header className="flex items-center justify-between px-6 py-5 border-b border-plum2">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-full bg-amber flex items-center justify-center text-ink font-display font-semibold">
          W
        </div>
        <div>
          <h1 className="font-display text-lg text-paper leading-none">Wavelength Support</h1>
          <p className="text-xs text-fog mt-1">Catalog &amp; billing, handled by a small team of agents</p>
        </div>
      </div>
      <div className="flex items-center gap-4 text-xs text-fog">
        {agentLabel && (
          <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-plum2 px-3 py-1">
            <span className="h-1.5 w-1.5 rounded-full bg-amber" />
            {agentLabel}
          </span>
        )}
        {customerId && (
          <span className="rounded-full bg-plum2 px-3 py-1 text-paper">Customer #{customerId}</span>
        )}
      </div>
    </header>
  );
}
