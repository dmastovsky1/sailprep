/** Arrow pointing where the wind is blowing to (meteorological direction + 180). */
export function WindArrow({ deg, className = "h-4 w-4" }: { deg: number; className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={`${className} inline-block shrink-0`}
      style={{ transform: `rotate(${deg + 180}deg)` }}
      aria-hidden
    >
      <path d="M12 3 6 13h4v8h4v-8h4L12 3Z" fill="currentColor" />
    </svg>
  );
}
