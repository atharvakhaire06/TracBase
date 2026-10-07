import type { SelectHTMLAttributes } from "react";

type SelectOption = {
  label: string;
  value: string;
};

type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string;
  options: SelectOption[];
  placeholder?: string;
};

export function Select({ label, id, options, placeholder, className = "", ...props }: SelectProps) {
  const selectId = id ?? (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

  return (
    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700" htmlFor={selectId}>
      {label ? <span>{label}</span> : null}
      <div className="relative w-full">
        <select
          id={selectId}
          className={`w-full appearance-none rounded-2xl border border-slate-200 bg-white px-4 py-3 pr-10 text-slate-900 shadow-sm outline-none transition-all duration-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 disabled:bg-slate-50 disabled:text-slate-400 ${className}`.trim()}
          {...props}
        >
          {placeholder ? (
            <option value="" disabled hidden>
              {placeholder}
            </option>
          ) : null}
          {options.map((option) => (
            <option key={option.value} value={option.value} className="bg-white text-slate-900 font-normal py-1">
              {option.label}
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
          <svg className="h-4 w-4 fill-current" viewBox="0 0 20 20">
            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
          </svg>
        </div>
      </div>
    </label>
  );
}
